from django.core.validators import validate_slug
from django.db import models

from users.models import Account


class Class(models.Model):
    name = models.CharField('Название', max_length=50)
    slug = models.SlugField(max_length=200, unique=True, validators=[validate_slug])

    users = models.ManyToManyField(Account, related_name='classes', blank=True)

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'
        ordering = ['name']

    def __str__(self):
        return self.name


def make_plain(text):
    if not text:
        text = ""
    plain = text.lower()
    plain = plain.replace('[b]', '').replace('[/b]', '').replace('[i]', '').replace('[/i]', '')
    plain = "".join([i for i in plain if i not in """,.:;-_»«[]"'!#-_"""])
    return plain


class Card(models.Model):
    image = models.ImageField(upload_to='cards', verbose_name='Карта')

    name = models.CharField('Название', max_length=50)
    plain_name = models.CharField('Очищенное название', max_length=50)
    text = models.CharField('Текст', max_length=1000, null=True, blank=True, default="")
    plain_text = models.CharField('Очищенный текст', max_length=1000, null=True, blank=True, default="")

    mana = models.SmallIntegerField('Мана')
    attack = models.SmallIntegerField('Атака', null=True, blank=True)
    health = models.SmallIntegerField('Здоровье', null=True, blank=True)

    card_type = models.CharField('Тип карты', max_length=25)
    race = models.CharField('Раса', max_length=25, null=True, blank=True)
    rarity = models.CharField('Редкость', max_length=25)

    cl = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='cards', verbose_name='Класс')
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='cards', null=True,
                             blank=True, verbose_name='Пользователь')

    def save(self, *args, **kwargs):
        self.plain_name = make_plain(self.name)
        self.plain_text = make_plain(self.text)

        if not self.attack:
            self.attack = None
        if not self.health:
            self.health = None

        super(Card, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'
        ordering = ['name']

    def __str__(self):
        return self.name
