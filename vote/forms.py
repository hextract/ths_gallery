from django import forms

from vote.models import Vote


class VoteForm(forms.ModelForm):
    design = forms.ChoiceField(choices=((i, i) for i in range(0, 11)), label='Внешний вид')
    balance = forms.ChoiceField(choices=((i, i) for i in range(0, 11)), label='Баланс')
    idea = forms.ChoiceField(choices=((i, i) for i in range(0, 11)), label='Идея')

    theme_like = forms.ChoiceField(choices=((i, i) for i in range(0, 6)), label='Соответствие теме')
    in_game = forms.ChoiceField(choices=((i, i) for i in range(0, 6)), label='Видение в игре')

    class Meta:
        model = Vote
        fields = ('theme_like', 'design', 'balance', 'idea', 'in_game', 'comment')
        widgets = {Vote.comment.field.name: forms.Textarea()}
