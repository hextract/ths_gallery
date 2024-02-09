import json
import random
import string

from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from gallery.settings import THS_KEY
from users.forms import SignInForm
from users.models import Account


def sign_in(request):
    form = SignInForm(request.POST or None)
    context = {
        'form': form,
    }

    if request.method == 'POST' and form.is_valid():
        for user in Account.objects.all():
            if user.check_password(form.cleaned_data['password']):
                code = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(100)])
                user.set_password(code)
                user.save()
                login(request, user)
                return redirect('/')
        context['error'] = 'Неверный код'

    return render(request, 'users/login.html', context)


@csrf_exempt
def set_code(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode("utf-8"))

        if 'Auth-token' in request.headers and request.headers['Auth-token'] == THS_KEY:
            user = Account.objects.filter(username=body['user_id'])
            if not user:
                user = Account.objects.create(username=body['user_id'],
                                              first_name=body['first_name'],
                                              last_name=body['last_name'])
            else:
                user = user.first()
            code = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(5)])
            user.set_password(code)
            user.save()

            return JsonResponse({'code': code}, safe=False)

    return JsonResponse({}, safe=False)