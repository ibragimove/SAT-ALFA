from django.core.management.base import BaseCommand
from core.models import (
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
)


class Command(BaseCommand):
    help = "Seeds database with demo content in Uzbek, English, and Russian"

    def handle(self, *args, **options):
        self.stdout.write("Seeding demo data...")

        # 1. TextBlocks (46 keys)
        text_blocks = {
            'nav_about': {
                'uz': "Biz haqimizda",
                'en': "About Us",
                'ru': "О нас",
            },
            'nav_advantages': {
                'uz': "Afzalliklar",
                'en': "Advantages",
                'ru': "Преимущества",
            },
            'nav_teachers': {
                'uz': "O'qituvchilar",
                'en': "Teachers",
                'ru': "Преподаватели",
            },
            'nav_prices': {
                'uz': "Narxlar",
                'en': "Prices",
                'ru': "Тарифы",
            },
            'nav_results': {
                'uz': "Natijalar",
                'en': "Results",
                'ru': "Результаты",
            },
            'nav_events': {
                'uz': "Tadbirlar",
                'en': "Events",
                'ru': "Мероприятия",
            },
            'nav_location': {
                'uz': "Manzil",
                'en': "Location",
                'ru': "Локация",
            },
            'nav_faq': {
                'uz': "FAQ",
                'en': "FAQ",
                'ru': "FAQ",
            },
            'hero_cta': {
                'uz': "Bepul darsga yozilish",
                'en': "Book a Free Lesson",
                'ru': "Записаться на пробный урок",
            },
            'about_title': {
                'uz': "SAT ALFA HAQIDA",
                'en': "ABOUT SAT ALFA",
                'ru': "О SAT ALFA",
            },
            'about_video_label': {
                'uz': "Markazimiz bo'ylab video sayohat",
                'en': "Video tour of our center",
                'ru': "Видео-экскурсия по нашему центру",
            },
            'advantages_title': {
                'uz': "NEGA AYNAN SAT ALFA?",
                'en': "WHY CHOOSE SAT ALFA?",
                'ru': "ПОЧЕМУ SAT ALFA?",
            },
            'events_banner_title': {
                'uz': "YANGI GURUH QABULI",
                'en': "NEW GROUP ADMISSION",
                'ru': "НАБОР В НОВЫЕ ГРУППЫ",
            },
            'events_banner_line1': {
                'uz': "Keyingi SAT imtihoniga 60 kunda tayyorlaning!",
                'en': "Prepare for the next SAT exam in 60 days!",
                'ru': "Подготовьтесь к следующему SAT за 60 дней!",
            },
            'events_banner_line2': {
                'uz': "Bepul diagnostik test topshiring va o'z darajangizni biling.",
                'en': "Take a free diagnostic test and check your level.",
                'ru': "Пройдите бесплатный диагностический тест и узнайте свой уровень.",
            },
            'events_banner_cta': {
                'uz': "Joy band qilish",
                'en': "Reserve a Seat",
                'ru': "Забронировать место",
            },
            'teachers_title': {
                'uz': "BIZNING O'QITUVCHILAR",
                'en': "OUR TEACHERS",
                'ru': "НАШИ ПРЕПОДАВАТЕЛИ",
            },
            'teachers_subtitle': {
                'uz': "1500+ ballga ega va xalqaro tajribali SAT instruktorlari",
                'en': "SAT instructors with 1500+ scores and international experience",
                'ru': "Инструкторы SAT с баллами 1500+ и международным опытом",
            },
            'label_sat_score': {
                'uz': "SAT balli",
                'en': "SAT score",
                'ru': "Балл SAT",
            },
            'label_experience': {
                'uz': "Tajriba",
                'en': "Experience",
                'ru': "Опыт",
            },
            'label_students': {
                'uz': "O'quvchilar",
                'en': "Students",
                'ru': "Студенты",
            },
            'tariffs_offline_title': {
                'uz': "OFFLINE TARIFLAR",
                'en': "OFFLINE TARIFFS",
                'ru': "ОФЛАЙН ТАРИФЫ",
            },
            'tariffs_online_title': {
                'uz': "ONLINE TARIFLAR",
                'en': "ONLINE TARIFFS",
                'ru': "ОНЛАЙН ТАРИФЫ",
            },
            'tariffs_cta_group': {
                'uz': "Guruhga yozilish",
                'en': "Join Group",
                'ru': "Записаться в группу",
            },
            'tariffs_cta_individual': {
                'uz': "Individual yozilish",
                'en': "Join Individual",
                'ru': "Индивидуальная запись",
            },
            'results_title': {
                'uz': "O'QUVCHILARIMIZ NATIJALARI",
                'en': "STUDENT RESULTS",
                'ru': "РЕЗУЛЬТАТЫ СТУДЕНТОВ",
            },
            'results_subtitle': {
                'uz': "O'quvchilarimiz dunyoning eng nufuzli universitetlariga qabul qilinmoqda",
                'en': "Our students gain admission to top world universities",
                'ru': "Наши студенты поступают в топовые мировые университеты",
            },
            'results_cta': {
                'uz': "Natijangizni yaxshilang",
                'en': "Improve Your Score",
                'ru': "Улучшите свой балл",
            },
            'results_view': {
                'uz': "To'liq ko'rish",
                'en': "View full result",
                'ru': "Смотреть полностью",
            },
            'events_title': {
                'uz': "TADBIRLAR VA MOCK TESTLAR",
                'en': "EVENTS & MOCK TESTS",
                'ru': "МЕРОПРИЯТИЯ И MOCK ТЕСТЫ",
            },
            'location_title': {
                'uz': "BIZNING MANZIL",
                'en': "OUR LOCATION",
                'ru': "НАШ АДРЕС",
            },
            'location_subtitle': {
                'uz': "Toshkent markazida qulay joylashuv va zamonaviy o'quv muhiti",
                'en': "Convenient central location in Tashkent with modern facilities",
                'ru': "Удобное расположение в центре Ташкента и современная учебная среда",
            },
            'location_open_google': {
                'uz': "Google Maps orqali ochish",
                'en': "Open in Google Maps",
                'ru': "Открыть в Google Maps",
            },
            'location_open_yandex': {
                'uz': "Yandex Xarita orqali ochish",
                'en': "Open in Yandex Maps",
                'ru': "Открыть в Яндекс Картах",
            },
            'label_address': {
                'uz': "Manzil",
                'en': "Address",
                'ru': "Адрес",
            },
            'label_hours': {
                'uz': "Ish vaqti",
                'en': "Working hours",
                'ru': "Режим работы",
            },
            'label_phone': {
                'uz': "Telefon",
                'en': "Phone",
                'ru': "Телефон",
            },
            'faq_title': {
                'uz': "KO'P BERILADIGAN SAVOLLAR",
                'en': "FREQUENTLY ASKED QUESTIONS",
                'ru': "ЧАСТО ЗАДАВАЕМЫЕ ВОПРОСЫ",
            },
            'contact_title': {
                'uz': "SAVOLLARINGIZ BORMI? BIZGA BOG'LANING!",
                'en': "HAVE QUESTIONS? CONTACT US!",
                'ru': "ОСТАЛИСЬ ВОПРОСЫ? СВЯЖИТЕСЬ С НАМИ!",
            },
            'form_name_placeholder': {
                'uz': "Ismingiz",
                'en': "Your name",
                'ru': "Ваше имя",
            },
            'form_phone_placeholder': {
                'uz': "Telefon raqamingiz",
                'en': "Your phone number",
                'ru': "Номер телефона",
            },
            'form_submit': {
                'uz': "Yuborish",
                'en': "Submit",
                'ru': "Отправить",
            },
            'form_success': {
                'uz': "Arizangiz muvaffaqiyatli qabul qilindi! Tez orada bog'lanamiz.",
                'en': "Your application has been received! We will contact you shortly.",
                'ru': "Ваша заявка успешно принята! Мы скоро свяжемся с вами.",
            },
            'form_error': {
                'uz': "Xatolik yuz berdi. Iltimos, ma'lumotlarni tekshiring.",
                'en': "An error occurred. Please check the details.",
                'ru': "Произошла ошибка. Пожалуйста, проверьте данные.",
            },
            'footer_rights': {
                'uz': "Barcha huquqlar himoyalangan.",
                'en': "All rights reserved.",
                'ru': "Все права защищены.",
            },
            'meta_title': {
                'uz': "SAT ALFA - Toshkentdagi SAT tayyorlov markazi",
                'en': "SAT ALFA - Premier SAT Preparation in Tashkent",
                'ru': "SAT ALFA - Центр подготовки к SAT в Ташкенте",
            },
            'meta_description': {
                'uz': "SAT imtihoniga professional tayyorgarlik. 1500+ ball to'plagan ustozlar va rasmiy mock testlar.",
                'en': "Professional SAT preparation in Tashkent. Instructors with 1500+ scores and official mock tests.",
                'ru': "Профессиональная подготовка к SAT в Ташкенте. Преподаватели с 1500+ и официальные mock-тесты.",
            },
        }

        for key, vals in text_blocks.items():
            TextBlock.objects.get_or_create(
                key=key,
                defaults={
                    'text': vals['uz'],
                    'text_uz': vals['uz'],
                    'text_en': vals['en'],
                    'text_ru': vals['ru'],
                },
            )

        # 2. SiteSettings (Single row)
        settings_defaults = {
            'phone': "+998 (71) 200-00-00",
            'email': "info@sat-alfa.uz",
            'telegram_url': "https://t.me/sat_alfa_fake",
            'instagram_url': "https://instagram.com/sat_alfa_fake",
            'youtube_url': "https://youtube.com/@sat_alfa_fake",
            'hero_title': "SAT bo'yicha orzuingizdagi 1500+ ballga erishing",
            'hero_title_uz': "SAT bo'yicha orzuingizdagi 1500+ ballga erishing",
            'hero_title_en': "Achieve your dream 1500+ SAT score",
            'hero_title_ru': "Получите заветные 1500+ на экзамене SAT",
            'hero_subtitle': "Toshkentdagi yetakchi ekspertlar bilan maqsadli va samarali tayyorgarlik",
            'hero_subtitle_uz': "Toshkentdagi yetakchi ekspertlar bilan maqsadli va samarali tayyorgarlik",
            'hero_subtitle_en': "Targeted and effective preparation with Tashkent's top test prep experts",
            'hero_subtitle_ru': "Целенаправленная и эффективная подготовка с ведущими экспертами Ташкента",
            'address': "Toshkent sh., Mirobod t., Amir Temur shoh ko'chasi, 100-uy",
            'address_uz': "Toshkent sh., Mirobod t., Amir Temur shoh ko'chasi, 100-uy",
            'address_en': "100 Amir Temur Avenue, Mirabad District, Tashkent",
            'address_ru': "г. Ташкент, Мирабадский р-н, проспект Амира Темура, д. 100",
            'working_hours': "Dushanba - Shanba: 09:00 - 20:00",
            'working_hours_uz': "Dushanba - Shanba: 09:00 - 20:00",
            'working_hours_en': "Monday - Saturday: 09:00 - 20:00",
            'working_hours_ru': "Понедельник - Суббота: 09:00 - 20:00",
            'map_embed_url': "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2996.9!2d69.28!3d41.31!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNDHCsDE4JzM2LjAiTiA2OcKwMTYnNDguMCJF!5e0!3m2!1sen!2suz!4v1234567890",
            'map_link': "https://maps.google.com",
        }
        site_settings = SiteSettings.objects.first()
        if site_settings:
            for attr, val in settings_defaults.items():
                setattr(site_settings, attr, val)
            site_settings.save()
        else:
            SiteSettings.objects.create(**settings_defaults)

        # 3. Stats (4 rows)
        stats_data = [
            {
                'value': "1520",
                'label_uz': "O'rtacha eng yuqori ball",
                'label_en': "Top Average Score",
                'label_ru': "Средний топовый балл",
                'note_uz': "Top 1% talabalar",
                'note_en': "Top 1% percentile",
                'note_ru': "Топ 1% студентов",
            },
            {
                'value': "1200+",
                'label_uz': "Muvaffaqiyatli bitiruvchilar",
                'label_en': "Successful Alumni",
                'label_ru': "Успешных выпускников",
                'note_uz': "2020-yildan buyon",
                'note_en': "Since 2020",
                'note_ru': "С 2020 года",
            },
            {
                'value': "98%",
                'label_uz': "Grant yutish ko'rsatkichi",
                'label_en': "Scholarship Rate",
                'label_ru': "Поступление на грант",
                'note_uz': "AQSH va Yevropa OTMlarida",
                'note_en': "In US & European unis",
                'note_ru': "В вузах США и Европы",
            },
            {
                'value': "15+",
                'label_uz': "Tajribali mentorlar",
                'label_en': "Expert Mentors",
                'label_ru': "Опытных наставников",
                'note_uz': "SAT 1500+ sohiblari",
                'note_en': "All scored 1500+",
                'note_ru': "С личным баллом 1500+",
            },
        ]
        for item in stats_data:
            Stat.objects.update_or_create(
                value=item['value'],
                defaults={
                    'label': item['label_uz'],
                    'label_uz': item['label_uz'],
                    'label_en': item['label_en'],
                    'label_ru': item['label_ru'],
                    'note': item['note_uz'],
                    'note_uz': item['note_uz'],
                    'note_en': item['note_en'],
                    'note_ru': item['note_ru'],
                },
            )

        # 4. Advantages (6 rows, 1 highlighted)
        advantages_data = [
            {
                'order': 1,
                'is_highlighted': True,
                'title_uz': "Rasmiy Digital SAT Simulyatsiyasi",
                'title_en': "Official Digital SAT Simulation",
                'title_ru': "Официальная симуляция Digital SAT",
                'text_uz': "Bluebook platformasi bilan 100% mos interfeys va haftalik to'liq test sinovlari.",
                'text_en': "100% Bluebook-compatible test interface and weekly full-length mock exams.",
                'text_ru': "100% совместимый с Bluebook интерфейс и еженедельные пробные тесты.",
            },
            {
                'order': 2,
                'is_highlighted': False,
                'title_uz': "Faqat 1500+ Balli Mentorlar",
                'title_en': "Mentors with 1500+ Scores Only",
                'title_ru': "Только преподаватели с 1500+",
                'text_uz': "Barcha o'qituvchilarimiz imtihonni shaxsan a'lo topshirgan amaliyotchi ekspertlardir.",
                'text_en': "All our instructors have personally mastered the test with 99th percentile scores.",
                'text_ru': "Все наши преподаватели лично сдали экзамен на высшие баллы.",
            },
            {
                'order': 3,
                'is_highlighted': False,
                'title_uz': "Shaxsiy Xatolar Tahlili",
                'title_en': "Personalized Mistake Analytics",
                'title_ru': "Персональный анализ ошибок",
                'text_uz': "Sun'iy intellekt asosidagi diagnostika har bir o'quvchining zaif nuqtalarini aniqlaydi.",
                'text_en': "AI-assisted diagnostics pinpoint every student's weak areas and provide custom drills.",
                'text_ru': "Диагностика точно определяет слабые зоны каждого студента.",
            },
            {
                'order': 4,
                'is_highlighted': False,
                'title_uz': "Kichik Guruhlar (8-10 kishi)",
                'title_en': "Small Groups (8-10 students)",
                'title_ru': "Мини-группы (8-10 человек)",
                'text_uz': "Har bir o'quvchiga yetarli e'tibor va individual yondashuv kafolatlanadi.",
                'text_en': "Individual attention and deep feedback for every student in every session.",
                'text_ru': "Индивидуальный подход и максимум внимания каждому ученику.",
            },
            {
                'order': 5,
                'is_highlighted': False,
                'title_uz': "To'liq O'quv Materiallari",
                'title_en': "Comprehensive Study Materials",
                'title_ru': "Полный комплект материалов",
                'text_uz': "Qo'shimcha kitob sotib olish shart emas: barcha rasmiy qo'llanmalar taqdim etiladi.",
                'text_en': "No need to buy external books: all official prep materials are provided.",
                'text_ru': "Не нужно покупать учебники: все официальные материалы включены.",
            },
            {
                'order': 6,
                'is_highlighted': False,
                'title_uz': "Kollejga Qabul Konsultatsiyasi",
                'title_en': "College Admission Guidance",
                'title_ru': "Консультация по поступлению",
                'text_uz': "Universitet tanlash va grantlarga hujjat topshirish bo'yicha bepul yo'l-yo'riq.",
                'text_en': "Free orientation on university selection and financial aid applications.",
                'text_ru': "Бесплатная помощь с выбором вуза и подачей на гранты.",
            },
        ]
        for adv in advantages_data:
            Advantage.objects.update_or_create(
                order=adv['order'],
                defaults={
                    'title': adv['title_uz'],
                    'title_uz': adv['title_uz'],
                    'title_en': adv['title_en'],
                    'title_ru': adv['title_ru'],
                    'text': adv['text_uz'],
                    'text_uz': adv['text_uz'],
                    'text_en': adv['text_en'],
                    'text_ru': adv['text_ru'],
                    'is_highlighted': adv['is_highlighted'],
                    'is_active': True,
                },
            )

        # 5. Teachers (6 rows, no photos)
        teachers_data = [
            {'name': "Azizbek Rahimov", 'sat_score': "1570", 'experience': "5 yil", 'students': "450+", 'order': 1},
            {'name': "Malika Yusupova", 'sat_score': "1550", 'experience': "4 yil", 'students': "380+", 'order': 2},
            {'name': "Jasur Karimov", 'sat_score': "1560", 'experience': "6 yil", 'students': "600+", 'order': 3},
            {'name': "Madina Aliyeva", 'sat_score': "1540", 'experience': "3 yil", 'students': "290+", 'order': 4},
            {'name': "Temur Rustamov", 'sat_score': "1580", 'experience': "7 yil", 'students': "750+", 'order': 5},
            {'name': "Shahzoda Umarova", 'sat_score': "1530", 'experience': "4 yil", 'students': "320+", 'order': 6},
        ]
        for tch in teachers_data:
            Teacher.objects.update_or_create(
                name=tch['name'],
                defaults={
                    'sat_score': tch['sat_score'],
                    'experience': tch['experience'],
                    'students': tch['students'],
                    'order': tch['order'],
                    'is_active': True,
                },
            )

        # 6. TariffPlans (4 rows) with 5 features each
        tariffs_data = [
            {
                'section': 'offline',
                'kind': 'group',
                'order': 1,
                'title_uz': "Offline Guruh",
                'title_en': "Offline Group",
                'title_ru': "Офлайн Группа",
                'price': "1 800 000 UZS / oy",
                'price_note_uz': "Haftada 3 kun, 2 soatdan",
                'price_note_en': "3 days/week, 2 hrs/session",
                'price_note_ru': "3 раза в неделю по 2 часа",
                'features': [
                    {'uz': "8-10 kishilik qulay auditoriya", 'en': "Modern classroom with 8-10 students", 'ru': "Современная аудитория на 8-10 человек", 'order': 1},
                    {'uz': "Haftalik rasmiy Mock testlar", 'en': "Weekly official Mock exams", 'ru': "Еженедельные официальные Mock тесты", 'order': 2},
                    {'uz': "Barcha bosma o'quv qo'llanmalari", 'en': "All printed course materials included", 'ru': "Все печатные учебные пособия", 'order': 3},
                    {'uz': "Coworking zonasidan bepul foydalanish", 'en': "Free access to study coworking zone", 'ru': "Бесплатный доступ в коворкинг", 'order': 4},
                    {'uz': "Yopiq Telegram guruhida 24/7 yordam", 'en': "24/7 mentor support in Telegram group", 'ru': "Поддержка наставника 24/7 в Telegram", 'order': 5},
                ],
            },
            {
                'section': 'offline',
                'kind': 'individual',
                'order': 2,
                'title_uz': "Offline Individual",
                'title_en': "Offline Individual",
                'title_ru': "Офлайн Индивидуально",
                'price': "3 800 000 UZS / oy",
                'price_note_uz': "Moslashuvchan jadval, 12 dars",
                'price_note_en': "Flexible schedule, 12 lessons",
                'price_note_ru': "Гибкий график, 12 занятий",
                'features': [
                    {'uz': "O'qituvchi bilan 1-ga-1 shaxsiy darslar", 'en': "1-on-1 private lessons with mentor", 'ru': "Индивидуальные уроки 1-на-1 с ментором", 'order': 1},
                    {'uz': "Darajangizga moslashtirilgan dastur", 'en': "Custom curriculum based on your target", 'ru': "Персональная программа под вашу цель", 'order': 2},
                    {'uz': "Xatolarni chuqur individual tahlil qilish", 'en': "Deep individual mistake breakdown", 'ru': "Глубокий разбор персональных ошибок", 'order': 3},
                    {'uz': "Istalgan vaqtda mock test topshirish", 'en': "Take mock exams whenever convenient", 'ru': "Сдача пробных тестов в любое время", 'order': 4},
                    {'uz': "Kollej insholari (essay) bo'yicha maslahat", 'en': "College application essay feedback", 'ru': "Помощь с эссе для поступления", 'order': 5},
                ],
            },
            {
                'section': 'online',
                'kind': 'group',
                'order': 3,
                'title_uz': "Online Guruh",
                'title_en': "Online Group",
                'title_ru': "Онлайн Группа",
                'price': "1 200 000 UZS / oy",
                'price_note_uz': "Zoom orqali jonli darslar",
                'price_note_en': "Live interactive Zoom sessions",
                'price_note_ru': "Живые уроки через Zoom",
                'features': [
                    {'uz': "Interaktiv jonli darslar va yozuvlar", 'en': "Interactive live classes with recordings", 'ru': "Интерактивные уроки и видеозаписи", 'order': 1},
                    {'uz': "Onlayn raqamli test platformasi", 'en': "Digital test practice platform", 'ru': "Доступ к онлайн тест-платформе", 'order': 2},
                    {'uz': "Raqamli darsliklar va PDF materiallar", 'en': "Digital textbooks and curated PDFs", 'ru': "Электронные учебники и PDF материалы", 'order': 3},
                    {'uz': "Uyga vazifalar avtomatik tekshiruvi", 'en': "Automated homework verification", 'ru': "Автоматическая проверка домашних заданий", 'order': 4},
                    {'uz': "Mentor bilan haftalik savol-javoblar", 'en': "Weekly live Q&A with mentor", 'ru': "Еженедельные онлайн Q&A с ментором", 'order': 5},
                ],
            },
            {
                'section': 'online',
                'kind': 'individual',
                'order': 4,
                'title_uz': "Online Individual",
                'title_en': "Online Individual",
                'title_ru': "Онлайн Индивидуально",
                'price': "2 900 000 UZS / oy",
                'price_note_uz': "To'liq shaxsiy online reja",
                'price_note_en': "100% personalized online roadmap",
                'price_note_ru': "Полностью индивидуальный онлайн план",
                'features': [
                    {'uz': "1-ga-1 online jonli mashg'ulotlar", 'en': "1-on-1 live sessions via Zoom/Meet", 'ru': "Уроки 1-на-1 через Zoom/Meet", 'order': 1},
                    {'uz': "Dars vaqtlari o'quvchi xohishiga ko'ra", 'en': "Schedule tailored to your timezone", 'ru': "Расписание под удобное вам время", 'order': 2},
                    {'uz': "Shaxsiy xatolar drayvi va haftalik hisobot", 'en': "Personal error log and progress reports", 'ru': "Личный лог ошибок и отчеты прогресса", 'order': 3},
                    {'uz': "Cheksiz raqamli test topshirish imkoni", 'en': "Unlimited digital practice tests", 'ru': "Неограниченные практические тесты", 'order': 4},
                    {'uz': "Universitet arizalari strategiyasi", 'en': "College application strategy session", 'ru': "Стратегическая сессия по поступлению", 'order': 5},
                ],
            },
        ]
        for tplan in tariffs_data:
            plan_obj, _ = TariffPlan.objects.update_or_create(
                section=tplan['section'],
                kind=tplan['kind'],
                defaults={
                    'title': tplan['title_uz'],
                    'title_uz': tplan['title_uz'],
                    'title_en': tplan['title_en'],
                    'title_ru': tplan['title_ru'],
                    'price': tplan['price'],
                    'price_note': tplan['price_note_uz'],
                    'price_note_uz': tplan['price_note_uz'],
                    'price_note_en': tplan['price_note_en'],
                    'price_note_ru': tplan['price_note_ru'],
                    'order': tplan['order'],
                    'is_active': True,
                },
            )
            for feat in tplan['features']:
                TariffFeature.objects.update_or_create(
                    plan=plan_obj,
                    order=feat['order'],
                    defaults={
                        'text': feat['uz'],
                        'text_uz': feat['uz'],
                        'text_en': feat['en'],
                        'text_ru': feat['ru'],
                        'is_active': True,
                    },
                )

        # 7. Results (6 rows, no images, score e.g. '1500')
        results_data = [
            {'student_name': "Sardorbek Olimov", 'score': "1560", 'order': 1},
            {'student_name': "Kamola Tursunova", 'score': "1530", 'order': 2},
            {'student_name': "Davron Ibrohimov", 'score': "1580", 'order': 3},
            {'student_name': "Nilufar Rahimova", 'score': "1510", 'order': 4},
            {'student_name': "Bekzod Mirzayev", 'score': "1550", 'order': 5},
            {'student_name': "Ziyoda Qodirova", 'score': "1520", 'order': 6},
        ]
        for res in results_data:
            Result.objects.update_or_create(
                student_name=res['student_name'],
                defaults={
                    'score': res['score'],
                    'order': res['order'],
                    'is_active': True,
                },
            )

        # 8. Events (6 rows)
        events_data = [
            {
                'order': 1,
                'date': "2026-12-01",
                'title_uz': "To'liq Digital SAT Mock Imtihoni",
                'title_en': "Full Digital SAT Mock Exam",
                'title_ru': "Полный пробный Digital SAT Mock",
                'desc_uz': "Haqiqiy imtihon sharoitida o'z bilimingizni sinab ko'ring.",
                'desc_en': "Test your knowledge under authentic exam conditions.",
                'desc_ru': "Проверьте свои знания в реальных условиях экзамена.",
            },
            {
                'order': 2,
                'date': "2026-12-08",
                'title_uz': "SAT Math 800 Masterklass",
                'title_en': "SAT Math 800 Masterclass",
                'title_ru': "Мастер-класс: SAT Math на 800",
                'desc_uz': "Eng qiyin algebra va geometriya savollarini yechish sirlari.",
                'desc_en': "Secret strategies to conquer the hardest algebra & geometry questions.",
                'desc_ru': "Секреты решения сложнейших задач по алгебре и геометрии.",
            },
            {
                'order': 3,
                'date': "2026-12-15",
                'title_uz': "AQSH Grantlari Vebinari",
                'title_en': "US Scholarships Webinar",
                'title_ru': "Вебинар: Гранты в вузы США",
                'desc_uz': "SAT orqali 100% grant yutib olish bosqichlari.",
                'desc_en': "Step-by-step roadmap to winning full-ride scholarships with the SAT.",
                'desc_ru': "Пошаговый план получения 100% гранта с помощью SAT.",
            },
            {
                'order': 4,
                'date': "2026-12-22",
                'title_uz': "Reading & Writing Tezkor Texnikalari",
                'title_en': "Reading & Writing Speed Strategies",
                'title_ru': "Быстрые техники Reading & Writing",
                'desc_uz': "Matnni tez tushunish va vaqtni to'g'ri taqsimlash usullari.",
                'desc_en': "How to read faster, analyze arguments, and eliminate trap answers.",
                'desc_ru': "Как быстрее читать текст и избегать вопросов-ловушек.",
            },
            {
                'order': 5,
                'date': "2027-01-05",
                'title_uz': "Ochiq Eshiklar Kuni",
                'title_en': "Open Doors Day",
                'title_ru': "День открытых дверей",
                'desc_uz': "Ustozlar bilan uchrashuv va bepul diagnostik test.",
                'desc_en': "Meet the faculty and take a complimentary diagnostic test.",
                'desc_ru': "Встреча с преподавателями и бесплатный вводный тест.",
            },
            {
                'order': 6,
                'date': "2027-01-10",
                'title_uz': "Intensiv Qishki SAT Oromgohi",
                'title_en': "Intensive Winter SAT Bootcamp",
                'title_ru': "Интенсивный зимний SAT буткемп",
                'desc_uz': "10 kunlik to'liq immersion tayyorgarlik kursi.",
                'desc_en': "10-day high-intensity immersion prep camp.",
                'desc_ru': "10-дневный интенсивный курс полного погружения.",
            },
        ]
        for ev in events_data:
            Event.objects.update_or_create(
                order=ev['order'],
                defaults={
                    'title': ev['title_uz'],
                    'title_uz': ev['title_uz'],
                    'title_en': ev['title_en'],
                    'title_ru': ev['title_ru'],
                    'date': ev['date'],
                    'description': ev['desc_uz'],
                    'description_uz': ev['desc_uz'],
                    'description_en': ev['desc_en'],
                    'description_ru': ev['desc_ru'],
                    'is_active': True,
                },
            )

        # 9. FAQs (6 rows)
        faqs_data = [
            {
                'order': 1,
                'q_uz': "Digital SAT kurslari qancha davom etadi?",
                'q_en': "How long do the Digital SAT courses last?",
                'q_ru': "Сколько длится курс подготовки к Digital SAT?",
                'a_uz': "Standart kursimiz 2 oydan 3 oygacha davom etadi. Dastlabki bilim darajasiga qarab individual muddatlar belgilanishi mumkin.",
                'a_en': "Our standard course runs from 2 to 3 months depending on your starting diagnostic score.",
                'a_ru': "Стандартный курс длится от 2 до 3 месяцев в зависимости от начального уровня.",
            },
            {
                'order': 2,
                'q_uz': "Kursga qatnashish uchun ingliz tili darajasi qanday bo'lishi kerak?",
                'q_en': "What English level is required to join?",
                'q_ru': "Какой уровень английского требуется для старта?",
                'a_uz': "SAT kursiga muvaffaqiyatli kirishish uchun kamida Intermediate (B1/B2) darajasi tavsiya etiladi.",
                'a_en': "We recommend at least an Intermediate (B1/B2) level for optimal progress.",
                'a_ru': "Рекомендуется уровень не ниже Intermediate (B1/B2) для уверенного старта.",
            },
            {
                'order': 3,
                'q_uz': "Mock testlar necha marta o'tkaziladi?",
                'q_en': "How often are mock exams conducted?",
                'q_ru': "Как часто проводятся пробные mock-тесты?",
                'a_uz': "Har haftaning yakshanba kuni markazimizda rasmiy formatdagi to'liq mock test o'tkaziladi va tahlil qilinadi.",
                'a_en': "Full-length mock exams are held every Sunday, followed by an in-depth review.",
                'a_ru': "Каждое воскресенье проводится полноценный mock-тест с последующим разбором ошибок.",
            },
            {
                'order': 4,
                'q_uz': "Darslarni o'tkazib yuborsam nima bo'ladi?",
                'q_en': "What if I miss a lesson?",
                'q_ru': "Что если я пропущу занятие?",
                'a_uz': "Barcha asosiy nazariy materiallar va dars yozuvlari shaxsiy kabinetda saqlanadi, shuningdek mentor bilan qo'shimcha konsultatsiya olishingiz mumkin.",
                'a_en': "Recorded lessons and class notes are available online, and you can schedule a catch-up review.",
                'a_ru': "Записи занятий и материалы доступны онлайн, также предусмотрена консультация с наставником.",
            },
            {
                'order': 5,
                'q_uz': "To'lovni bo'lib to'lash imkoni bormi?",
                'q_en': "Is installment payment available?",
                'q_ru': "Есть ли возможность оплаты в рассрочку?",
                'a_uz': "Ha, to'lovni oylik asosda yoki butun kurs uchun chegirma bilan to'lash mumkin.",
                'a_en': "Yes, you can pay monthly or pay upfront for the full course with a discount.",
                'a_ru': "Да, вы можете оплачивать ежемесячно или оплатить весь курс со скидкой.",
            },
            {
                'order': 6,
                'q_uz': "Birinchi dars bepulmi?",
                'q_en': "Is the first trial lesson free?",
                'q_ru': "Первый пробный урок бесплатный?",
                'a_uz': "Ha, siz birinchi sinov darsi va diagnostik testda mutlaqo bepul qatnashishingiz mumkin.",
                'a_en': "Yes, the diagnostic test and the first trial lesson are completely free of charge.",
                'a_ru': "Да, пробный урок и первичный диагностический тест совершенно бесплатны.",
            },
        ]
        for faq in faqs_data:
            FAQ.objects.update_or_create(
                order=faq['order'],
                defaults={
                    'question': faq['q_uz'],
                    'question_uz': faq['q_uz'],
                    'question_en': faq['q_en'],
                    'question_ru': faq['q_ru'],
                    'answer': faq['a_uz'],
                    'answer_uz': faq['a_uz'],
                    'answer_en': faq['a_en'],
                    'answer_ru': faq['a_ru'],
                    'is_active': True,
                },
            )

        # Summary of row counts
        self.stdout.write(self.style.SUCCESS("Demo content seeded successfully!"))
        self.stdout.write(f"TextBlock: {TextBlock.objects.count()}")
        self.stdout.write(f"SiteSettings: {SiteSettings.objects.count()}")
        self.stdout.write(f"Stat: {Stat.objects.count()}")
        self.stdout.write(f"Advantage: {Advantage.objects.count()}")
        self.stdout.write(f"Teacher: {Teacher.objects.count()}")
        self.stdout.write(f"TariffPlan: {TariffPlan.objects.count()}")
        self.stdout.write(f"TariffFeature: {TariffFeature.objects.count()}")
        self.stdout.write(f"Result: {Result.objects.count()}")
        self.stdout.write(f"Event: {Event.objects.count()}")
        self.stdout.write(f"FAQ: {FAQ.objects.count()}")
