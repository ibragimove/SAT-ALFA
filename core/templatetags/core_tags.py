from django import template
from django.urls import translate_url
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from core.models import TextBlock

register = template.Library()


@register.simple_tag(takes_context=True)
def t(context, key):
    request = context.get('request')
    lang = get_language() or 'uz'

    if request is not None:
        if not hasattr(request, '_textblock_cache'):
            request._textblock_cache = {tb.key: tb for tb in TextBlock.objects.all()}
        tb = request._textblock_cache.get(key)
    else:
        tb = TextBlock.objects.filter(key=key).first()

    if not tb:
        return key

    val = getattr(tb, f'text_{lang}', None) or getattr(tb, 'text', None)
    return mark_safe(val) if val else key


@register.simple_tag(takes_context=True)
def lang_url(context, lang_code):
    request = context.get('request')
    if not request:
        return f'/{lang_code}/'
    full_path = request.get_full_path()
    translated = translate_url(full_path, lang_code)
    return translated if translated else f'/{lang_code}/'
