"""Tests for flag language switcher dropdown (FIX I)."""
import re
from django.test import TestCase


class LanguageSwitcherTests(TestCase):
    """Verify the flag language switcher in /uz/, /en/ and /ru/."""

    def test_pages_return_200_and_contain_language_links(self):
        """GET /uz/, /en/ and /ru/ return 200 and contain three language rows with correct URLs, labels, and flags."""
        languages = [
            ('uz', "O'zbek", 'flags/uz.svg'),
            ('en', 'English', 'flags/gb.svg'),
            ('ru', 'Русский', 'flags/ru.svg'),
        ]

        for code, label, flag in languages:
            response = self.client.get(f'/{code}/')
            self.assertEqual(response.status_code, 200, f"/{code}/ returned {response.status_code}")
            html = response.content.decode()

            # Verify all three language links are present
            for target_code, target_label, target_flag in languages:
                self.assertIn(f'/{target_code}/', html, f"Link to /{target_code}/ missing on /{code}/")
                self.assertIn(target_label, html, f"Label {target_label} missing on /{code}/")
                self.assertIn(target_flag, html, f"Flag {target_flag} missing on /{code}/")

            # Check that old desktop switcher markup (like lang-divider) is completely gone
            self.assertNotIn('lang-divider', html)
            self.assertNotIn('UZ / EN / RU', html)

    def test_ru_page_has_active_russian_row_only(self):
        """On /ru/ the active row is the Russian one (active class and aria-current='true'), and not on others."""
        response = self.client.get('/ru/')
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()

        # Match all dropdown menu items inside lang-dropdown-menu
        menu_items = re.findall(r'<a[^>]+role="menuitem"[^>]*>.*?</a>', html, re.DOTALL)
        self.assertEqual(len(menu_items), 3, f"Expected 3 menu items, found {len(menu_items)}")

        for item in menu_items:
            if 'Русский' in item:
                self.assertTrue('active' in item or 'aria-current="true"' in item, "Russian row should be active on /ru/")
            elif 'English' in item:
                self.assertFalse('active' in item, "English row should not be active on /ru/")
                self.assertFalse('aria-current="true"' in item, "English row should not have aria-current on /ru/")
            elif "O'zbek" in item:
                self.assertFalse('active' in item, "Uzbek row should not be active on /ru/")
                self.assertFalse('aria-current="true"' in item, "Uzbek row should not have aria-current on /ru/")

    def test_en_page_has_active_english_row_only(self):
        """On /en/ the active row is the English one."""
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()

        menu_items = re.findall(r'<a[^>]+role="menuitem"[^>]*>.*?</a>', html, re.DOTALL)
        self.assertEqual(len(menu_items), 3)

        for item in menu_items:
            if 'English' in item:
                self.assertTrue('active' in item or 'aria-current="true"' in item)
            else:
                self.assertFalse('active' in item)
                self.assertFalse('aria-current="true"' in item)

    def test_uz_page_has_active_uzbek_row_only(self):
        """On /uz/ the active row is the Uzbek one."""
        response = self.client.get('/uz/')
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()

        menu_items = re.findall(r'<a[^>]+role="menuitem"[^>]*>.*?</a>', html, re.DOTALL)
        self.assertEqual(len(menu_items), 3)

        for item in menu_items:
            if "O'zbek" in item:
                self.assertTrue('active' in item or 'aria-current="true"' in item)
            else:
                self.assertFalse('active' in item)
                self.assertFalse('aria-current="true"' in item)
