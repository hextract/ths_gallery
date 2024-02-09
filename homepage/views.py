import random

from django.shortcuts import render

from cards.models import Card, make_plain
from homepage.forms import MainPageForm


def home(request):
    form = MainPageForm(request.POST or None, request.FILES or None)
    cards = Card.objects.order_by('cl__slug', 'mana', 'name')

    if request.POST and form.is_valid():
        if form.cleaned_data['attack']:
            if '-' in form.cleaned_data['attack']:
                data = form.cleaned_data['attack'].split('-')
                cards = cards.filter(attack__gte=int(data[0]), attack__lte=int(data[1]))
            else:
                cards = cards.filter(attack=form.cleaned_data['attack'])
                
        if form.cleaned_data['mana']:
            if '-' in form.cleaned_data['mana']:
                data = form.cleaned_data['mana'].split('-')
                cards = cards.filter(mana__gte=int(data[0]), mana__lte=int(data[1]))
            else:
                cards = cards.filter(mana=form.cleaned_data['mana'])

        if form.cleaned_data['health']:
            if '-' in form.cleaned_data['health']:
                data = form.cleaned_data['health'].split('-')
                cards = cards.filter(health__gte=int(data[0]), health__lte=int(data[1]))
            else:
                cards = cards.filter(health=form.cleaned_data['health'])

        if form.cleaned_data['search']:
            text = make_plain(form.cleaned_data['search'])
            cards = cards.filter(plain_text__icontains=text) | cards.filter(plain_name__contains=text)

        if form.cleaned_data['card_type'] != 'Любая':
            print(form.cleaned_data['card_type'])
            cards = cards.filter(card_type=form.cleaned_data['card_type'])

        if form.cleaned_data['rarity'] != 'Любая':
            cards = cards.filter(rarity=form.cleaned_data['rarity'])

        if form.cleaned_data['race'] and form.cleaned_data['race'] != 'Все':
            cards = cards.filter(race__icontains=form.cleaned_data['race'].lower()) | cards.filter(race__iexact='Все')

        if form.cleaned_data['classes']:
            cards = cards.filter(cl__in=form.cleaned_data['classes'])

        if form.cleaned_data['amount']:
            cards = random.sample(list(cards.all()), form.cleaned_data['amount'])

    context = {
        'form': form,
        'cards': cards if type(cards) is list else cards.all()
    }

    return render(request, 'homepage/index.html', context=context)