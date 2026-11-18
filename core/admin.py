from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline

from .models import (
    TextBlock,
    SiteSettings,
    Stat,
    Advantage,
    Teacher,
    TariffPlan,
    TariffFeature,
    Result,
    Event,
    FAQ,
    Application,
)

admin.site.site_header = 'SAT ALFA admin'
admin.site.site_title = 'SAT ALFA admin'


@admin.register(TextBlock)
class TextBlockAdmin(TabbedTranslationAdmin):
    list_display = ['key', 'text']
    search_fields = ['key']


@admin.register(SiteSettings)
class SiteSettingsAdmin(TabbedTranslationAdmin):
    list_display = ['__str__', 'phone', 'email']
    readonly_fields = ['hero_poster_preview', 'about_poster_preview']

    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description='Hero Poster Preview')
    def hero_poster_preview(self, obj):
        if obj.hero_poster:
            return format_html('<img src="{}" style="max-width: 150px; max-height: 100px; object-fit: cover; border-radius: 4px;" />', obj.hero_poster.url)
        return "-"

    @admin.display(description='About Poster Preview')
    def about_poster_preview(self, obj):
        if obj.about_poster:
            return format_html('<img src="{}" style="max-width: 150px; max-height: 100px; object-fit: cover; border-radius: 4px;" />', obj.about_poster.url)
        return "-"


@admin.register(Stat)
class StatAdmin(TabbedTranslationAdmin):
    list_display = ['value', 'label', 'note']


@admin.register(Advantage)
class AdvantageAdmin(TabbedTranslationAdmin):
    list_display = ['title', 'is_highlighted', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_highlighted', 'is_active']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'photo_preview', 'sat_score', 'experience', 'students', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    readonly_fields = ['photo_preview']

    @admin.display(description='Photo')
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />', obj.photo.url)
        return "-"


class TariffFeatureInline(TranslationTabularInline):
    model = TariffFeature
    extra = 1
    fields = ('text', 'order', 'is_active')


@admin.register(TariffPlan)
class TariffPlanAdmin(TabbedTranslationAdmin):
    list_display = ['title', 'section', 'kind', 'price', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['section', 'kind', 'is_active']
    inlines = [TariffFeatureInline]


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_preview', 'student_name', 'score', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    readonly_fields = ['image_preview']

    @admin.display(description='Image')
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "-"


@admin.register(Event)
class EventAdmin(TabbedTranslationAdmin):
    list_display = ['title', 'image_preview', 'date', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    readonly_fields = ['image_preview']

    @admin.display(description='Image')
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "-"


@admin.register(FAQ)
class FAQAdmin(TabbedTranslationAdmin):
    list_display = ['question', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'created_at', 'telegram_sent', 'ip']
    search_fields = ['name', 'phone']
    list_filter = ['created_at', 'telegram_sent']
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
