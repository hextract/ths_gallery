from django.urls import path

from cards import views

app_name = 'cards'

urlpatterns = [
    path('', views.list_of_cards, name='list'),
    path('create/', views.create_card, name='create_card'),
    path('create_api/', views.create_api, name='create_api'),
    path('file/', views.create_card_from_file_step_1, name='create_card_from_file_step_1'),
    path('file_save/', views.create_card_from_file_step_2, name='create_card_from_file_step_2'),
    path('edit/<int:pk>/', views.edit_card, name='edit_card'),
    path('delete/<int:pk>/', views.delete_card, name='delete_card'),
]
