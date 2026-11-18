from django.db import models


class Ordered(models.Model):
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['order', 'id']


class TextBlock(models.Model):
    key = models.SlugField(max_length=100, unique=True)
    text = models.TextField()

    def __str__(self):
        return self.key


class SiteSettings(models.Model):
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, blank=True)
    telegram_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    hero_video = models.FileField(upload_to='hero/', blank=True)
    hero_poster = models.ImageField(upload_to='hero/', blank=True)
    hero_title = models.CharField(max_length=255)
    hero_subtitle = models.CharField(max_length=255, blank=True)
    about_video = models.FileField(upload_to='about/', blank=True)
    about_poster = models.ImageField(upload_to='about/', blank=True)
    address = models.CharField(max_length=255)
    working_hours = models.CharField(max_length=255)
    map_embed_url = models.TextField(blank=True)
    map_link = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'Site Settings'


class Stat(models.Model):
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    note = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.value} {self.label}"


class Advantage(Ordered):
    title = models.CharField(max_length=255)
    text = models.TextField()
    is_highlighted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Teacher(Ordered):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='teachers/', blank=True)
    sat_score = models.CharField(max_length=50)
    experience = models.CharField(max_length=50)
    students = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class TariffPlan(Ordered):
    SECTION_CHOICES = [
        ('offline', 'Offline'),
        ('online', 'Online'),
    ]
    KIND_CHOICES = [
        ('group', 'Group'),
        ('individual', 'Individual'),
    ]

    section = models.CharField(max_length=20, choices=SECTION_CHOICES, default='offline')
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default='group')
    title = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    price_note = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.get_section_display()} - {self.get_kind_display()} ({self.title})"


class TariffFeature(Ordered):
    plan = models.ForeignKey(TariffPlan, on_delete=models.CASCADE, related_name='features')
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.plan.title} - {self.text}"


class Result(Ordered):
    image = models.ImageField(upload_to='results/')
    student_name = models.CharField(max_length=100, blank=True)
    score = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.student_name} ({self.score})" if self.student_name else self.score


class Event(Ordered):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='events/', blank=True)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class FAQ(Ordered):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question


class Application(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    telegram_sent = models.BooleanField(default=False)
    ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"
