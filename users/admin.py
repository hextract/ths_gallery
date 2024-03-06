from django.contrib import admin

from users.models import Account


@admin.register(Account)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_superuser', 'is_staff', 'can_vote', 'votes', 'average')

    def votes(self, obj):
        return obj.votes.count()

    def average(self, obj):
        return sum(i.result for i in obj.votes.all()) // max(obj.votes.count(), 1)
