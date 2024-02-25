import random

from django import forms

from users.models import Account


class SignInForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('password',)

        labels = {
            Account.password.field.name: 'Код входа:'
        }

        help_texts = {
            Account.password.field.name: """Можно получить в любом боте арены THS, например <a type="button"
                       href="https://vk.com/thsbarmen">тут</a> используя команду !вход"""
        }