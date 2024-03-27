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

    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    boost = models.IntegerField(verbose_name='Бонус', default=0)

    class Meta:
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'

    def __str__(self):
        return self.name


class VoteToken(models.Model):
    image = models.ImageField(upload_to='vote_tokens')
    card = models.ForeignKey(VoteCard, on_delete=models.CASCADE,
                             related_name='tokens')

    def __str__(self):
        return "token: " + self.card.name

    class Meta:
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'


class Vote(models.Model):
    theme_like = models.IntegerField(verbose_name='Соответствие теме')
    design = models.IntegerField(verbose_name='Внешний вид')
    balance = models.IntegerField(verbose_name='Баланс')
    idea = models.IntegerField(verbose_name='Идея')

    in_game = models.IntegerField(verbose_name='Видение в игре')

    comment = models.TextField(verbose_name='Комментарий')

    result = models.IntegerField(verbose_name='Итог', null=True, blank=True)

    card = models.ForeignKey(VoteCard, on_delete=models.CASCADE, related_name='votes', null=True, blank=True)

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='votes', null=True,
                             blank=True, verbose_name='Пользователь')

    def save(self, *args, **kwargs):
        self.result = round((int(self.design) + int(self.balance) +
                             int(self.idea)) * (1.0 + int(self.in_game) / 10)) * (1.0 - int(self.theme_like) / 10)
        super(Vote, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'

    def __str__(self):
        return self.user.get_full_name() + ': ' + self.card.name
