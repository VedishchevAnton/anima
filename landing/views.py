import requests
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render

from .data import (
    CONTACT_INFO,
    NAV_ITEMS,
    RENT_FEATURES,
    RENT_ITEMS,
    ROASTING_FEATURES,
    SELECTION_CARDS,
    SOCIAL_LINKS,
)


def check_recaptcha(gcaptcha):
    data = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': gcaptcha,
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = r.json()
    return result.get('success', False)


def index(request):
    context = {
        'page_title': 'Anima — техника для кофе в Екатеринбурге',
        'page_description': 'Обслуживание, ремонт, подбор, аренда кофейного оборудования',
        'csrf_token': get_token(request),
        'RECAPTCHA_SITE_KEY': settings.GOOGLE_RECAPTCHA_SITE_KEY,
        'nav_items': NAV_ITEMS,
        'social_links': SOCIAL_LINKS,
        'rent_features': RENT_FEATURES,
        'roasting_features': ROASTING_FEATURES,
        'selection_cards': SELECTION_CARDS,
        'contact_info': CONTACT_INFO,
        'rent_items': RENT_ITEMS,
    }
    return render(request, 'landing/index.html', context)


def feedback(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    gcaptcha = request.POST.get('g-recaptcha-response', '')
    if not gcaptcha or not check_recaptcha(gcaptcha):
        return JsonResponse({'status': False, 'error_captcha': 'Подтвердите, что вы не робот'})

    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()
    phone = request.POST.get('phone', '').strip()
    email = request.POST.get('email', '').strip()
    message = request.POST.get('message', '').strip()

    errors = {}
    if not first_name:
        errors['first_name'] = 'Введите имя'
    if not last_name:
        errors['last_name'] = 'Введите фамилию'
    if not phone or len(''.join(c for c in phone if c.isdigit())) < 11:
        errors['phone'] = 'Введите корректный номер телефона'
    if not email or '@' not in email:
        errors['email'] = 'Введите корректный e-mail'
    if not message:
        errors['message'] = 'Введите сообщение'

    if errors:
        return JsonResponse({'status': False, 'errors': errors})

    subject = 'Заявка с сайта Anima'
    body = (
        f'Имя: {first_name}\n'
        f'Фамилия: {last_name}\n'
        f'Телефон: {phone}\n'
        f'E-mail: {email}\n'
        f'Сообщение:\n{message}'
    )

    if settings.DEBUG:
        print('=' * 50)
        print(f'[FEEDBACK] {subject}')
        print(body)
        print('=' * 50)
    else:
        msg = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.FEEDBACK_EMAIL],
        )
        msg.send(fail_silently=False)

    return JsonResponse({'status': True, 'message': 'Заявка отправлена!'})
