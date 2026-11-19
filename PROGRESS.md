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

## Task 11: Responsive, accessibility, and performance pass
- Verified zero horizontal overflow across 360px, 768px, 1280px, and 1920px viewports with carousel wrapping safeguards.
- Enforced 44px minimum tap targets across mobile burger, close button, navigation links, language switcher, and social buttons.
- Ensured all images have descriptive alt text, added high-contrast :focus-visible outlines, and dynamic <html lang> attributes.
- Configured loading='lazy' on all content images and updated about-video to preload='metadata'.
- Implemented prefers-reduced-motion overrides disabling fade-up animations and carousel/anchor smooth scrolling.

## Task 12: Metadata, Error Pages, and Robots.txt
- Configured dynamic meta tags in templates/base.html: <title>, meta description, canonical URL, hreflang links (uz, en, ru, x-default), Open Graph properties, and favicon.
- Designed and built styled error pages templates/404.html and templates/500.html in black & yellow theme with return-to-home buttons (zero DB queries in 500.html).
- Implemented /robots.txt endpoint in core/views.py and core/urls.py returning plain text that allows all search engine indexing.
- Verified DEBUG=False styled 404 rendering, source verification of titles/canonical/hreflang across uz/en/ru, and confirmed all 10 project tests pass.


## FIX B: Application popup modal and floating apply button
- Created reusable form partial `templates/partials/_form.html` supporting configurable ID prefixes (`prefix='contact'` and `prefix='modal'`), preserving honeypot, CSRF, and form.js compatibility.
- Created `templates/partials/_modal.html` with `id="apply-modal"`, `role="dialog"`, `aria-modal="true"`, dark blurred backdrop, and centered card.
- Implemented modal open/close, backdrop click, Escape key dismiss, focus trap, and return-to-trigger focus in `static/js/main.js`.
- Added yellow floating form button with black message icon next to floating call button, plus `data-open-form` across hero CTA, tariffs, results, and floating button.
- Added test suite `core/tests_modal.py` validating 200 status, modal ID presence, at least 4 `data-open-form` elements, 2 honeypot inputs, and no duplicate IDs.


## FIX C: Dual form AJAX submission and modal auto-close
- Added `data-apply-form` attribute to `templates/partials/_form.html`.
- Updated `static/js/form.js` to dynamically select and bind submit handlers and phone masks independently to every application form using relative DOM queries, eliminating hardcoded single-form IDs.
- Added double-click protection (`isSubmitting` lock + button disable) and modal auto-close after 2.5s on successful submission (modal stays open on errors).
- Extended `core/tests_modal.py` with mock Telegram testing verifying dual form submission saving 2 Application records; all 17 tests pass.
- Command to run: `python manage.py test`.


## FIX E: Navbar text wrapping in Russian & Uzbek
- Updated `.navbar` in `static/css/main.css` to `flex-wrap: nowrap`, ensuring logo, links, phone, and switcher stay on a single row.
- Applied `white-space: nowrap` and `flex-shrink: 0` to brand logo text, phone number, and language switcher.
- Configured `.nav-links` as `flex: 1 1 auto` with fluid `gap: clamp(10px, 1.2vw, 26px)` and `margin: 0 16px` for spacing.
- Moved desktop navbar links breakpoint to `min-width: 1280px` (burger menu active below 1280px), with font scaling `clamp(12px, 0.8vw, 13.5px)` between 1280px and 1440px.
- Verified `python manage.py check` passes with 0 issues.


## FIX F: Navbar scrolled state yellow blur styling & IntersectionObserver
- Replaced scroll-distance listener with an `IntersectionObserver` observing `#hero` with `rootMargin: '-90px 0px 0px 0px'`, toggling `'is-scrolled'` on `#main-navbar` when `#about` reaches the navbar.
- Styled `.navbar.is-scrolled` with brand yellow blur `rgba(241, 255, 10, 0.78)` and `backdrop-filter: blur(16px) saturate(140%)` (solid `#F1FF0A` fallback under `@supports not`).
- Configured black `#0D0C11` text, phone, links, burger icon, and active switcher pill (`#0D0C11` background, `#F1FF0A` text) with 250ms smooth transition (disabled under `prefers-reduced-motion`).
- Removed all legacy white scrolled navbar background rules; verified `manage.py check` and all 17 tests pass.


## FIX G: Student name on every result card & layout parity
- Refactored `templates/partials/_results.html` to render a shared `.result-card-header` containing the 'OFFICIAL RESULT' badge and student name directly below it on every card.
- Updated `static/css/sections.css` with 2-line ellipsis clamping for `.result-student`, `object-fit: contain` white frame for `.result-card-media`, and baseline-aligned `.result-card-footer`.
- Cards with an image display the contained image in the middle area; cards without an image display the watermark and open space in `.result-card-cert`.
- Added test suite `core/tests_results.py` verifying name rendering for cards with and without images and empty-name handling; all 20 tests pass.


## FIX H: Result image lightbox modal & carousel drag threshold
- Added `data-lightbox`, `data-src`, `data-name`, `data-score` and a small black pill view button with `{% t 'results_view' %}` to image cards in `templates/partials/_results.html`.
- Created `templates/partials/_result_lightbox.html` and `static/js/lightbox.js` with focus trap, loading placeholder, backdrop dismiss, and prioritized Escape handler.
- Updated `static/js/carousel.js` with a 6px drag threshold to prevent clicks during carousel panning.
- Added `results_view` TextBlock to `seed_demo.py` and database (uz: "To'liq ko'rish", en: "View full result", ru: "Смотреть полностью").
- Extended `core/tests_results.py` with lightbox markup and data-lightbox existence tests; all 22 tests pass.


## FIX I: Flag language switcher dropdown & mobile language pills
- Created SVG flag assets in `static/img/flags/` (`gb.svg`, `uz.svg`, `ru.svg`).
- Created `templates/partials/_lang_switcher.html` featuring a 40px round pill button with current flag and chevron icon, opening an accessible right-aligned dropdown card with English, O'zbek, and Русский options.
- Added dropdown keyboard navigation (ArrowUp/ArrowDown, Enter, Space, Escape focus return), outside-click dismiss, and mobile pills inside the full-screen burger menu in `static/css/main.css` and `static/js/main.js`.
- Added test suite `core/tests_lang.py` verifying links, flags, active row selection, and removal of old text switcher; all 26 tests pass.
