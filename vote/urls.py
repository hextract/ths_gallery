from django.urls import path

from vote import views

app_name = 'vote'

urlpatterns = [
    path('', views.list_round, name='list_round'),
    path('new/<int:pk>/', views.new_vote, name='new_vote'),
]
