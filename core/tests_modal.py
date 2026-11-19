"""Tests for the application modal (FIX B)."""
import re
from collections import Counter
from django.test import TestCase
from core.models import SiteSettings, TariffPlan


class ModalTest(TestCase):
    """Verify modal markup on the home page."""

    def setUp(self):
        SiteSettings.objects.create(
            phone='+998901234567',
            hero_title='Preparation',
            address='Tashkent',
            working_hours='09:00 - 18:00'
        )
        TariffPlan.objects.create(
            section='offline',
            kind='group',
            title='Offline Group',
            price='1 200 000',
            order=1
        )
        TariffPlan.objects.create(
            section='online',
            kind='individual',
            title='Online Pro',
            price='2 000 000',
            order=2
        )
        self.response = self.client.get('/uz/')
        self.html = self.response.content.decode()

    def test_home_status(self):
        """GET /uz/ returns 200."""
        self.assertEqual(self.response.status_code, 200)

    def test_modal_present(self):
        """The HTML contains id='apply-modal'."""
        self.assertIn('id="apply-modal"', self.html)

    def test_data_open_form_count(self):
        """At least 4 elements with data-open-form."""
        count = len(re.findall(r'data-open-form', self.html))
        self.assertGreaterEqual(count, 4, f'Found only {count} data-open-form attributes')

    def test_honeypot_count(self):
        """Exactly 2 inputs named 'website' (one per form)."""
        count = len(re.findall(r'name=["\']website["\']', self.html))
        self.assertEqual(count, 2, f'Expected 2 honeypot inputs, found {count}')

    def test_no_duplicate_ids(self):
        """No id value appears twice in the page."""
        ids = re.findall(r'\bid=["\']([^"\']+)["\']', self.html)
        duplicates = {k: v for k, v in Counter(ids).items() if v > 1}
        self.assertEqual(len(duplicates), 0, f'Duplicate ids: {duplicates}')
