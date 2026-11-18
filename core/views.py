from django.shortcuts import render
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
