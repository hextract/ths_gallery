from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from vote.forms import VoteForm
from vote.models import Vote, VoteCard, Stage


def list_round(request):
    stage = request.GET.get('stage', 1)
    stage = get_object_or_404(Stage, pk=stage)
    if not request.user.is_authenticated or not request.user.can_vote:
        stages = len(Stage.objects.filter(shown=True).all())
        if not stage.shown:
            return render(request, 'vote/hidden.html', context={'stage': stage,
                                                      'stages': stages})
    else:
        stages = len(Stage.objects.all())

    cards = VoteCard.objects.filter(stage=stage)
    votes = {card.id: round(sum([i.result for i in card.votes.all()]) / max(1, len(card.votes.all()))) + card.boost for card in cards}

    return render(request, 'vote/list.html', context={'cards': cards, 'stage': stage,
                                                      'stages': stages, 'votes': votes})


@login_required
def new_vote(request, pk):
    if not request.user.can_vote:
        return redirect('users:login')

    card = VoteCard.objects.get(pk=int(pk))
    vote = Vote.objects.filter(user=request.user, card=card).first()
    if vote:
        form = VoteForm(request.POST or None, instance=vote)
    else:
        form = VoteForm(request.POST or None)

    context = {
        'card': card,
        'form': form,
    }

    if request.method == 'POST' and form.is_valid():
        vote = Vote.objects.filter(user=request.user, card=card).first()
        if vote:
            form.save()
        else:
            vote = Vote.objects.create(**form.cleaned_data)
            vote.user = request.user
            vote.card = card
            vote.save()

        return redirect(f'/vote/?stage={card.stage.id}')

    return render(request, 'vote/vote.html', context)