from django.urls import path

from deckview import views

app_name = 'cards'

urlpatterns = [
    path('', views.main, name='list'),
]
