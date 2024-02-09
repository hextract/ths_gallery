from django import forms

from cards.forms import CHOICES_RARITY, CHOICES_TYPE
from cards.models import Card, Class


class MainPageForm(forms.ModelForm):
    search = forms.CharField(label='Текст поиска',
                             widget=forms.TextInput(attrs={'placeholder': '"Боевой клич" или "Бранн Бронзобород"'}),
                             required=False)

    rarity = forms.ChoiceField(choices=((i, i) for i in ['Любая'] + CHOICES_RARITY), label='Редкость', required=False)
    card_type = forms.ChoiceField(choices=((i, i) for i in ['Любая'] + CHOICES_TYPE), label='Тип карты', required=False)

    classes = forms.ModelMultipleChoiceField(Class.objects.all().order_by('slug'), label='',
                                        widget=forms.CheckboxSelectMultiple(attrs={'class': "form-check"}),required=False)

    amount = forms.IntegerField(label='Кол-во:', required=False)

    mana = forms.CharField(label='Мана', max_length=10, required=False,
                           widget=forms.TextInput(attrs={'placeholder': '1-10'}))
    attack = forms.CharField(label='Атака', max_length=10, required=False,
                             widget=forms.TextInput(attrs={'placeholder': '1-10'}))
    health = forms.CharField(label='Здоровье', max_length=10, required=False,
                             widget=forms.TextInput(attrs={'placeholder': '1-10'}))

    class Meta:
        model = Card
        fields = ('card_type', 'race', 'rarity')
