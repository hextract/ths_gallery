from django.contrib import admin

from vote.models import Vote, VoteCard, Stage, VoteToken


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'result')


@admin.register(VoteCard)
class VoteCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'stage', 'boost')


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('theme', 'shown')


@admin.register(VoteToken)
class VoteTokenAdmin(admin.ModelAdmin):
    pass
