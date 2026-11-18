from modeltranslation.translator import register, TranslationOptions
from .models import (
    TextBlock,
    SiteSettings,
    Stat,
    Advantage,
    TariffPlan,
    TariffFeature,
    Event,
    FAQ,
)


@register(TextBlock)
class TextBlockTranslationOptions(TranslationOptions):
    fields = ('text',)


@register(SiteSettings)
class SiteSettingsTranslationOptions(TranslationOptions):
    fields = ('hero_title', 'hero_subtitle', 'address', 'working_hours')


@register(Stat)
class StatTranslationOptions(TranslationOptions):
    fields = ('label', 'note')


@register(Advantage)
class AdvantageTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


@register(TariffPlan)
class TariffPlanTranslationOptions(TranslationOptions):
    fields = ('title', 'price_note')


@register(TariffFeature)
class TariffFeatureTranslationOptions(TranslationOptions):
    fields = ('text',)


@register(Event)
class EventTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')
