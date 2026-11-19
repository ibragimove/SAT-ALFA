from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from .forms import ApplicationForm
from .models import (
    SiteSettings,
    Stat,
    Advantage,
    Teacher,
    TariffPlan,
    Result,
    Event,
    FAQ,
)
from .telegram import send_message


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def home(request):
    site_settings = SiteSettings.objects.first()
    stats = Stat.objects.all()
    advantages = Advantage.objects.filter(is_active=True)
    teachers = Teacher.objects.filter(is_active=True)
    tariff_plans = TariffPlan.objects.filter(is_active=True).prefetch_related('features')
    tariffs_offline = [p for p in tariff_plans if p.section == 'offline']
    tariffs_online = [p for p in tariff_plans if p.section == 'online']
    results = Result.objects.filter(is_active=True)
    events = Event.objects.filter(is_active=True)
    faqs = FAQ.objects.filter(is_active=True)

    context = {
        'site_settings': site_settings,
        'stats': stats,
        'advantages': advantages,
        'teachers': teachers,
        'tariff_plans': tariff_plans,
        'tariffs_offline': tariffs_offline,
        'tariffs_online': tariffs_online,
        'results': results,
        'events': events,
        'faqs': faqs,
    }
    return render(request, 'home.html', context)


@require_POST
def apply(request):
    # 1. Spam protection: Honeypot check
    website = request.POST.get('website', '').strip()
    if website:
        # Silently return success without saving
        return JsonResponse({'ok': True, 'message': 'Application received'})

    # 2. Rate limiting: 5 submissions per IP per 10 minutes (600s)
    ip = get_client_ip(request)
    cache_key = f"rate_limit_apply_{ip}"
    submission_count = cache.get(cache_key, 0)
    if submission_count >= 5:
        return JsonResponse(
            {'ok': False, 'error': 'Too many requests. Please try again later.'},
            status=429
        )

    # 3. Validate form data
    form = ApplicationForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'ok': False, 'errors': form.errors}, status=400)

    # Increment rate limit counter
    cache.set(cache_key, submission_count + 1, timeout=600)

    # 4. Save Application
    application = form.save(commit=False)
    application.ip = ip
    application.save()

    # 5. Send Telegram notification
    now_str = application.created_at.strftime('%Y-%m-%d %H:%M:%S')
    telegram_text = (
        f"New application\n"
        f"Name: {application.name}\n"
        f"Phone: {application.phone}\n"
        f"Time: {now_str}"
    )
    sent = send_message(telegram_text)
    if sent:
        application.telegram_sent = True
        application.save(update_fields=['telegram_sent'])

    # Always return success if saved, even if Telegram failed
    return JsonResponse({'ok': True, 'message': 'Application saved successfully'})


def robots(request):
    lines = [
        "User-agent: *",
        "Allow: /",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")

