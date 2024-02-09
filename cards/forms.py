from django import forms

from cards.models import Card

RARITIES = {
    'Free': 'Базовая',
    'Common': 'Обычная',
    'Rare': 'Редкая',
    'Epic': 'Эпическая',
    'Legendary': 'Легендарная'
}
CARD_TYPES = {
    'minion': 'Существо',
    'spell': 'Заклинание',
    'location': 'Локация',
    'weapon': 'Оружие',
    'herocard': 'Герой'
}

CHOICES_RARITY = list(RARITIES.values())
CHOICES_TYPE = list(CARD_TYPES.values())


class CardForm(forms.ModelForm):
    rarity = forms.ChoiceField(choices=((i, i) for i in CHOICES_RARITY), label='Редкость')
    card_type = forms.ChoiceField(choices=((i, i) for i in CHOICES_TYPE), label='Тип карты')

    class Meta:
        model = Card
        fields = ('image', 'name', 'text', 'mana', 'attack', 'health', 'card_type', 'race', 'rarity', 'cl')

        widgets = {Card.text.field.name: forms.Textarea()}


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class CardFileForm(forms.Form):
    cl = forms.ChoiceField(choices=(), label='Класс')
    files = MultipleFileField(label='Файлы из Hearthcards')


class CardImagesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        cards = kwargs.pop('cards')
        super(CardImagesForm, self).__init__(*args, **kwargs)

        for card in cards:
            self.fields[f'card_{card}'] = forms.FileField(label=card)
