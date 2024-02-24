from django.contrib import admin

from vote.models import Vote, VoteCard, Stage, VoteToken


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    pass


@admin.register(VoteCard)
class VoteCardAdmin(admin.ModelAdmin):
    pass


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    pass


@admin.register(VoteToken)
class VoteTokenAdmin(admin.ModelAdmin):
    pass
