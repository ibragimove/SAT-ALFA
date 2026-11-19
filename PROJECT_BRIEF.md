# PROJECT BRIEF

## PROJECT
You are building 'SAT ALFA', a single-page marketing website with an admin panel for an SAT preparation learning center in Uzbekistan. One page, one branch, three languages (Uzbek default, English, Russian). Visitors read the page and submit a form (name + phone) that is saved in the database and sent to a Telegram bot.

## STACK (add nothing else without asking)
- Python 3.12, Django 5.x, MySQL (mysqlclient), django-modeltranslation, Pillow, whitenoise, gunicorn, requests, python-dotenv
- Django templates, plain CSS, vanilla JavaScript. No React, Tailwind, Bootstrap, jQuery or npm.
- Project package: config. One app: core.

## DESIGN - the look to copy
Reference: the layout and feel of inter-nation.uz, restyled in black and yellow.
- Colors (CSS variables): --yellow #F1FF0A; --black #0D0C11; --white #FFFFFF; --bg #F4F4F2 (light sections); --gray-text #5B5B63; --success #22C55E (form success only). Never use yellow as text on white or light backgrounds (poor contrast): headings on light backgrounds are black.
- Font: Inter (Google Fonts) with system sans-serif fallback. Headings: weight 800, uppercase, centered, clamp(28px, 4vw, 44px). Body 16-18px.
- Shape: big rounded corners (cards 24px, buttons and inputs fully rounded), soft shadows, generous spacing, content max-width 1580px (like inter-nation.uz on a 1920px screen), side padding 16px mobile / 24px tablet / 32px desktop. The navbar uses the same width as the content container.
- Buttons: primary = solid yellow, bold black text, rounded-full, small sparkle icon (inline SVG) on the left. Secondary = black background, yellow text. Hover = slight lift.
- Navbar: floating rounded-full pill, fixed at the top with 16px margin. The navbar uses the same width as the content container. Over the hero it stays translucent dark with blur and white text. After scrolling past the hero it turns solid yellow (#F1FF0A) with black text and a soft shadow (NOT white). Icons (burger, language switcher) become black. Link hover = black pill with yellow text. Left: logo + text 'SAT ALFA'. Center: anchor links (About, Advantages, Teachers, Prices, Results, Events, Location, FAQ). Right: phone number + language switcher (UZ / EN / RU). No user icon, no Vacancy, no Public offer. Mobile: burger button opening a full-screen black menu.
- Floating buttons: two round buttons at the bottom-right, side by side with a 12px gap: (a) the call button (black, yellow phone icon, links to tel:), (b) the form button right next to it (yellow with a black message icon, aria-label 'Apply') that opens the application modal.
- Application modal: a centered popup with a dark blurred backdrop, white card (24px radius), title, name input, phone input with +998 mask, yellow submit button and a close (X) button. It opens from ANY element with the attribute data-open-form (hero CTA, tariff buttons, results button, floating form button). It closes on X, backdrop click or Escape; page scroll is locked while open; focus moves to the name input and stays inside the modal. The contact card in the FAQ section stays and uses the same form partial and the same endpoint.
- Decoration: soft abstract yellow blobs/curves (inline SVG or CSS gradients) in corners of some light sections, behind content, low z-index, never blocking clicks.
- Section order: Hero (video) > About (light) > Advantages (white) > Teachers (light) > Tariffs Offline (white) > Tariffs Online (light) > Results (white) > Events (light) > Location (white) > FAQ + contact form (light) > Footer (black).
- Hero: full-screen background video (autoplay, muted, loop, playsinline) with a dark gradient overlay. Bottom-left: title (line 1 yellow 'SAT ALFA', line 2 white), one-line subtitle, yellow CTA button that scrolls to the form or opens the application modal via data-open-form. If no video is uploaded, show a black gradient.
- Cards: white, 24px radius, soft shadow. One highlighted dark card (black background, yellow heading) in Advantages.
- Teacher card: portrait photo fills the card, dark gradient at the bottom, uppercase name, small pill chips with label + value (SAT score, Experience, Students).
- Tariff cards: two per section (Group, Individual). Header block: yellow with black text (Group) and black with yellow text (Individual), big price, feature list with bolt icons, full-width black button that opens the modal via data-open-form or scrolls to #contact.
- Results and Events: horizontal scroll-snap carousels with prev/next buttons and swipe/drag.
- FAQ: white rounded rows, plus icon rotates into a cross when open, smooth open/close, one open at a time.
- Contact card: 'Still have questions? Contact us!' with a name input, a phone input (+998 mask) and a yellow button.
- Footer: black, logo, social icons, copyright.
- Motion: subtle fade-up on scroll (IntersectionObserver). Respect prefers-reduced-motion.

## CONTENT RULES
- All visible text comes from the database in uz/en/ru and is editable in the admin. Fixed texts (nav labels, buttons, headings, placeholders) live in a TextBlock model, read with a {% t 'key' %} template tag. No gettext .po files.
- No external images. Placeholder media = CSS gradients or inline SVG.
- Placeholder content comes from the seed command (Task 4).

## WORKING RULES (strict - these prevent bugs)
1. Do ONLY the task I paste. No extra features, no 'improvements', no refactoring of earlier work.
2. Touch only the files the task lists. If you need another file, stop and ask.
3. Add no dependencies beyond STACK. If an install fails, stop and report the exact error.
4. Keep code simple and readable. No abstractions you do not need yet.
5. When finished, run the task's DONE WHEN commands, paste their output, and mark each item PASS or FAIL. Fix only failures caused by this task.
6. If blocked or unsure, stop and ask ONE clear question instead of guessing.
7. After Task 2, never change models or edit existing migrations unless told to.
8. At the end of each task, append 3-5 lines to PROGRESS.md (what was done, what to run).
