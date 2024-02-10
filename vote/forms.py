from django import forms

from vote.models import Vote


class VoteForm(forms.ModelForm):
    design = forms.ChoiceField(choices=((i, i) for i in range(0, 11)), label='Дизайн')
    balance = forms.ChoiceField(choices=((i, i) for i in range(0, 11)), label='Баланс')
    realisation = forms.ChoiceField(choices=((i, i) for i in range(0, 11)), label='Реализация')

    mistakes = forms.ChoiceField(choices=((i, i) for i in range(0, 6)), label='Ошибки')
    idea = forms.ChoiceField(choices=((i, i) for i in range(0, 6)), label='Идея')

    class Meta:
        model = Vote
        fields = ('mistakes', 'design', 'balance', 'realisation', 'idea', 'comment')
        widgets = {Vote.comment.field.name: forms.Textarea()}
