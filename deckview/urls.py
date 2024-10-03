from django.urls import path

from deckview import views

app_name = 'deckview'

urlpatterns = [
    path('', views.main, name='list'),
]
