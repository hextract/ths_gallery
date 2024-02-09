from django.urls import path

from users.views import sign_in, set_code

app_name = 'users'

urlpatterns = [
    path('login/', sign_in, name='login'),
    path('set_code/', set_code, name='set_code')
]
