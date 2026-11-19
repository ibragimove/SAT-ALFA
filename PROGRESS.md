# SAT ALFA - Progress

## Task 1: Runnable empty Django project
- Initialized Django 5.x project 'config' with app 'core' and virtual environment.
- Configured MySQL connection (utf8mb4), localization (uz/en/ru, Asia/Tashkent), WhiteNoise, and media serving.
- Created .env.example, .gitignore, static/templates folders, and committed initial structure to git.
- Commands to run: `python manage.py check`, `python manage.py migrate`, `python manage.py runserver`.

## Task 2: Create all database models
- Added modeltranslation to INSTALLED_APPS before django.contrib.admin.
- Created Ordered abstract base model and all 11 core models with __str__ methods.
- Registered translatable fields (uz, en, ru) in core/translation.py and generated initial migration 0001_initial.py.
- Successfully applied migration to MySQL and verified field presence and ORM operations in shell.

## Task 3: Configure Django admin
- Configured TabbedTranslationAdmin for translated models, TabularInline for TariffFeature, and list_editable for Ordered models.
- Configured SiteSettings singleton restrictions, read-only Application admin, and image thumbnail previews.
- Added admin changelist test suite in core/tests_admin.py and verified passing tests and clean system check.
- Command to run: `python manage.py test core.tests_admin`.

## Task 4: Seed demo data management command
- Created management command `seed_demo` in core/management/commands/seed_demo.py.
- Seeded all 46 TextBlock keys, SiteSettings, Stats, Advantages, Teachers, TariffPlans, TariffFeatures, Results, Events, and FAQs in uz, en, and ru.
- Verified command idempotency (running twice produces identical row counts) and verified translation tabs in admin.
- Command to run: `python manage.py seed_demo`.

## Task 5: Page skeleton, language URLs, navbar and CSS design system
- Configured i18n_patterns with prefix_default_language=True, root '/' redirect to '/uz/', and core.urls routing.
- Implemented {% t 'key' %} with request-level caching and {% lang_url 'code' %} template tags.
- Built base.html, partials/_navbar.html, partials/_footer.html, home.html with all 10 section IDs, CSS design system, and JS.
- Verified /uz/, /en/, /ru/ return 200 with matching translated nav labels, pill navbar styling, and check passes.

## Task 6: Hero, About, and Advantages sections
- Built partials/_hero.html with video background/poster, dark overlay, SiteSettings hero title/subtitle, yellow CTA, and black gradient fallback.
- Built partials/_about.html with left video card (poster, play button, in-place play handler in main.js) and right Stats grid with decorative yellow accents.
- Built partials/_advantages.html with 3-col/1-col Advantage grid (dark highlighted card) and full-width yellow events banner with sparkles and CTA.
- Added sections.css, verified responsive rendering with seed data at 375px/1280px in uz/en/ru, and confirmed dynamic Stat updates reflect immediately.

## Task 7: Teachers and Tariffs sections
- Created partials/_teachers.html featuring responsive card grid (5 cols desktop, 3 tablet, 2 mobile) with gradient placeholder + initials fallback, uppercase names, and chips for SAT score, experience, and students.
- Created reusable partials/_tariffs.html used for both #tariffs-offline and #tariffs-online, rendering Group (yellow header) and Individual (black header) cards with prices, price notes, bolt-icon features, and full-width CTA buttons.
- Appended styling and soft yellow decorative shapes to static/css/sections.css.
- Verified 4 tariff cards render across uz/en/ru, dynamic price updates reflect immediately, and verified zero horizontal overflow at 375px.

## Task 8: Results and Events horizontal carousels
- Created static/js/carousel.js with CSS scroll-snap, prev/next navigation buttons with auto-disabled states, and smooth mouse-drag support for all elements with `data-carousel`.
- Built partials/_results.html with Results cards on yellow gradients, prominent score number typography, certificate watermark fallback when no image is present, and black CTA button to #contact.
- Built partials/_events.html with Event poster cards in 3:4 ratio, date badges, titles, descriptions, and sleek dark gradient fallback.
- Linked carousel.js in base.html and appended all carousel and card styling to static/css/sections.css.

## Task 9: Location, FAQ Accordion, Contact Card, and Footer
- Built partials/_location.html featuring map embed/iframe next to detailed info card (address, hours, phone) and Google/Yandex maps action buttons.
- Built partials/_faq.html with FAQ accordion (smooth animation, one open at a time, plus rotates into cross) and Contact card (#contact) with name, phone (+998 mask), and yellow submit button.
- Updated partials/_footer.html with brand logo, dynamic social icons (Telegram, Instagram, YouTube when defined in SiteSettings), and copyright text.
- Added accordion toggle and +998 (XX) XXX-XX-XX input mask in main.js, verified clean rendering across uz/en/ru without console errors.

## Task 10: Contact form submission and Telegram notifications
- Created core/forms.py with ApplicationForm validating name (2-100 chars) and phone (+998 followed by exactly 9 digits).
- Created core/telegram.py sending formatted, HTML-escaped Telegram alerts with a 5s timeout without raising on network failures.
- Implemented core/views.py 'apply' POST-only endpoint with CSRF check, honeypot protection, 5 reqs/10 min IP rate limiting, DB save, and Telegram alert.
- Created static/js/form.js for AJAX submission with CSRF header, button disabling, form reset, and translated status messages.
- Added comprehensive test suite in core/tests_apply.py (7 tests covering valid save, bad phone, honeypot, and 429 rate limit); all 10 project tests pass.
