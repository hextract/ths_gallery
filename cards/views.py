import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from cards.forms import CardForm, CardFileForm, CardImagesForm, RARITIES, CARD_TYPES
from cards.models import Card, Class


def get_user_classes(user):
    return user.classes.all() if not user.is_superuser else Class.objects.all()


@login_required
def list_of_cards(request):
    my_classes = get_user_classes(request.user)

    cards = Card.objects.filter(cl__in=my_classes).order_by('-id').all()[:10]

    return render(request, 'cards/list.html', context={'cards': cards})


@login_required
def delete_card(request, pk):
    card = get_object_or_404(Card, pk=pk)

    if request.user.is_superuser or card.cl in request.user.classes.all():
        card.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def edit_card(request, pk):
    card = get_object_or_404(Card, pk=pk)

    if request.user.is_superuser or card.cl in request.user.classes.all():
        form = CardForm(request.POST or None, request.FILES or None, instance=card)
        form.fields['cl'].queryset = get_user_classes(request.user)

        context = {
            'form': form,
        }

        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('homepage:home')

        return render(request, 'cards/card.html', context)

    return redirect('homepage:home')


@login_required
def create_card(request):
    form = CardForm(request.POST or None, request.FILES or None)
    form.fields['cl'].queryset = get_user_classes(request.user)
    context = {
        'form': form,
    }

    if request.method == 'POST' and form.is_valid():
        card = Card.objects.create(**form.cleaned_data)
        card.user = request.user
        card.save()

        return redirect('cards:list')

    return render(request, 'cards/card.html', context)


@csrf_exempt
def create_api(request):
    form = CardForm(request.POST or None, request.FILES or None)
    form.fields['cl'].choices = ((i.id, i.id) for i in Class.objects.all())

    if request.method == 'POST' and form.is_valid():
        Card.objects.create(**form.cleaned_data)

        return JsonResponse({'success': True}, safe=False)

    return JsonResponse({'success': False}, safe=False)


@login_required
def create_card_from_file_step_1(request):
    form = CardFileForm(request.POST or None, request.FILES or None)
    form.fields['cl'].choices = ((i.id, i.name) for i in get_user_classes(request.user))

    context = {
        'form': form,
    }

    if request.method == 'POST' and form.is_valid():
        files = request.FILES.getlist('files')

        cards = {}

        for file in files:
            data = json.load(file)

            card = {
                'image': 'No image:(',

                'name': data['Title'],
                'text': data['Text'],
                'cl_id': int(form.cleaned_data['cl']),

                'rarity': RARITIES[data['Rarity']],
                'card_type': CARD_TYPES[data['Type']],
                'race': data['Tribe'].lower(),

                'mana': data['Cost']['Value'],
                'health': data['Health'],
                'attack': data['Attack'],

                'user_id': request.user.id
            }
            cards[data['Title']] = card
            request.session['cards'] = cards

        return redirect('cards:create_card_from_file_step_2')

    return render(request, 'cards/files_1.html', context)


@login_required
def create_card_from_file_step_2(request):
    cards = request.session.get('cards')
    if cards:
        form = CardImagesForm(request.POST or None, request.FILES or None,
                              cards=cards.keys())
        context = {
            'form': form,
        }

        if request.method == 'POST' and form.is_valid():
            for file in request.FILES:
                cards[file[5:]]['image'] = request.FILES[file]
                Card.objects.create(**cards[file[5:]])

            return redirect('cards:list')

        return render(request, 'cards/files_2.html', context)

    else:
        return redirect('cards:list')
