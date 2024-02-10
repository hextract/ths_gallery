from django.db import models

from users.models import Account


class Stage(models.Model):
    id = models.IntegerField(verbose_name='Номер раунда', primary_key=True)

    theme = models.CharField(max_length=100, verbose_name='Тема')

    shown = models.BooleanField(default=False, verbose_name='Показан?')

    class Meta:
        verbose_name = 'Раунд'
        verbose_name_plural = 'Раунды'

    def __str__(self):
        return str(self.id) + ": " + self.theme


class VoteCard(models.Model):
    image = models.ImageField(upload_to='vote_cards', verbose_name='Карта')
    name = models.CharField('Название', max_length=50)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, verbose_name='Раунд')

    boost = models.IntegerField(verbose_name='Бонус', default=0)

    class Meta:
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'

    def __str__(self):
        return self.name


class Vote(models.Model):
    mistakes = models.IntegerField(verbose_name='Ошибки')
    design = models.IntegerField(verbose_name='Дизайн')
    balance = models.IntegerField(verbose_name='Баланс')
    realisation = models.IntegerField(verbose_name='Реализация')

    idea = models.IntegerField(verbose_name='Идея')

    comment = models.TextField(verbose_name='Комментарий')

    result = models.IntegerField(verbose_name='Итог', null=True, blank=True)

    card = models.ForeignKey(VoteCard, on_delete=models.CASCADE, related_name='votes', null=True, blank=True)

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='votes', null=True,
                             blank=True, verbose_name='Пользователь')

    def save(self, *args, **kwargs):
        self.result = round((int(self.design) + int(self.balance) +
                             int(self.realisation)) * (1.0 + int(self.idea) / 10)) * (1.0 - int(self.mistakes) / 10)
        super(Vote, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'

    def __str__(self):
        return self.user.get_full_name() + ': ' + self.card.name
