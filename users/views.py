import json
import string
from datetime import timedelta
from secrets import choice

from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.crypto import salted_hmac
from django.views.decorators.csrf import csrf_exempt

from gallery.settings import THS_KEY
from users.forms import SignInForm
from users.models import Account, SignInCode


def sign_in_code_digest(code):
    return salted_hmac('users.sign_in_code', code, algorithm='sha256').hexdigest()


def sign_in(request):
    form = SignInForm(request.POST or None)
    context = {
        'form': form,
    }

    if request.method == 'POST' and form.is_valid():
        digest = sign_in_code_digest(form.cleaned_data['password'])
        with transaction.atomic():
            code = SignInCode.objects.select_related('account').filter(
                digest=digest,
                expires_at__gt=timezone.now(),
                account__is_active=True,
            ).first()
            if code:
                consumed, _ = SignInCode.objects.filter(
                    pk=code.pk,
                    digest=digest,
                    expires_at__gt=timezone.now(),
                ).delete()
                if consumed:
                    login(request, code.account)
                    return redirect('/')
        context['error'] = 'Неверный код'

    return render(request, 'users/login.html', context)


@csrf_exempt
def set_code(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode("utf-8"))

        if 'Auth-token' in request.headers and request.headers['Auth-token'] == THS_KEY:
            user, _ = Account.objects.get_or_create(
                username=body['user_id'],
                defaults={
                    'first_name': lambda: body['first_name'],
                    'last_name': lambda: body['last_name'],
                    'password': lambda: make_password(None),
                },
            )
            alphabet = string.ascii_letters + string.digits
            for _ in range(5):
                code = ''.join(choice(alphabet) for _ in range(5))
                digest = sign_in_code_digest(code)
                try:
                    SignInCode.objects.update_or_create(
                        account=user,
                        defaults={'digest': digest, 'expires_at': timezone.now() + timedelta(minutes=10)},
                    )
                except IntegrityError:
                    if not SignInCode.objects.filter(digest=digest).exists():
                        raise
                else:
                    return JsonResponse({'code': code}, safe=False)
            return JsonResponse({}, status=503)

    return JsonResponse({}, safe=False)
