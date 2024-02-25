from django.contrib import admin

from users.models import Account


@admin.register(Account)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_superuser', 'is_staff', 'can_vote')
