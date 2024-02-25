from django.contrib import admin

from cards.models import Card, Class


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'cl')


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    filter_horizontal = ('users',)
