"""Tests for the application modal (FIX B) and dual form handling (FIX C)."""
import re
from collections import Counter
from unittest import mock
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from core.models import SiteSettings, TariffPlan, Application


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

    def test_data_apply_form_count(self):
        """Both forms have the data-apply-form attribute."""
        count = len(re.findall(r'data-apply-form', self.html))
        self.assertEqual(count, 2, f'Expected 2 forms with data-apply-form, found {count}')

    def test_apply_both_forms_saves_two_rows(self):
        """POST a valid name and phone to the apply endpoint twice (as the two forms would) with Telegram mocked -> 2 Application rows saved."""
        cache.clear()
        apply_url = reverse('core:apply')

        with mock.patch('core.views.send_message', return_value=True) as mock_send:
            # First submission (contact card form)
            resp1 = self.client.post(
                apply_url,
                {'name': 'Contact User', 'phone': '+998 (90) 111-22-33'},
                HTTP_HOST='127.0.0.1'
            )
            self.assertEqual(resp1.status_code, 200)
            self.assertTrue(resp1.json().get('ok'))

            # Second submission (popup modal form)
            resp2 = self.client.post(
                apply_url,
                {'name': 'Modal User', 'phone': '+998 (91) 444-55-66'},
                HTTP_HOST='127.0.0.1'
            )
            self.assertEqual(resp2.status_code, 200)
            self.assertTrue(resp2.json().get('ok'))

        self.assertEqual(Application.objects.count(), 2)
        self.assertEqual(mock_send.call_count, 2)

        apps = list(Application.objects.order_by('id'))
        self.assertEqual(apps[0].name, 'Contact User')
        self.assertEqual(apps[0].phone, '+998901112233')
        self.assertEqual(apps[1].name, 'Modal User')
        self.assertEqual(apps[1].phone, '+998914445566')

