from unittest import mock
from django.core.cache import cache
from django.test import TestCase, Client
from django.urls import reverse
from core.models import Application


class ApplyViewTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client()
        # Use localized or direct url
        self.url = reverse('core:apply')

    def test_valid_post_saves_and_sends_telegram(self):
        with mock.patch('core.views.send_message', return_value=True) as mock_send:
            response = self.client.post(
                self.url,
                {'name': "Azizbek Rahimov", 'phone': "+998 (90) 123-45-67"},
                HTTP_HOST='127.0.0.1'
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json().get('ok'))

        self.assertEqual(Application.objects.count(), 1)
        app = Application.objects.first()
        self.assertEqual(app.name, "Azizbek Rahimov")
        self.assertEqual(app.phone, "+998901234567")
        self.assertTrue(app.telegram_sent)

        mock_send.assert_called_once()
        sent_text = mock_send.call_args[0][0]
        self.assertIn("New application", sent_text)
        self.assertIn("Azizbek Rahimov", sent_text)
        self.assertIn("+998901234567", sent_text)

    def test_valid_post_saves_even_if_telegram_fails(self):
        with mock.patch('core.views.send_message', return_value=False) as mock_send:
            response = self.client.post(
                self.url,
                {'name': "Malika Yusupova", 'phone': "+998 99 987 65 43"},
                HTTP_HOST='127.0.0.1'
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json().get('ok'))

        self.assertEqual(Application.objects.count(), 1)
        app = Application.objects.first()
        self.assertEqual(app.name, "Malika Yusupova")
        self.assertEqual(app.phone, "+998999876543")
        self.assertFalse(app.telegram_sent)
        mock_send.assert_called_once()

    def test_bad_phone_returns_400(self):
        response = self.client.post(
            self.url,
            {'name': "Jasur Karimov", 'phone': "12345"},
            HTTP_HOST='127.0.0.1'
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json().get('ok'))
        self.assertEqual(Application.objects.count(), 0)

    def test_short_name_returns_400(self):
        response = self.client.post(
            self.url,
            {'name': "A", 'phone': "+998 90 123 45 67"},
            HTTP_HOST='127.0.0.1'
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json().get('ok'))
        self.assertEqual(Application.objects.count(), 0)

    def test_honeypot_saves_nothing(self):
        response = self.client.post(
            self.url,
            {
                'name': "Spam Bot",
                'phone': "+998 90 123 45 67",
                'website': "https://spam-link.com",
            },
            HTTP_HOST='127.0.0.1'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json().get('ok'))
        self.assertEqual(Application.objects.count(), 0)

    def test_rate_limit_sixth_post_returns_429(self):
        with mock.patch('core.views.send_message', return_value=True):
            # First 5 submissions must succeed
            for i in range(5):
                resp = self.client.post(
                    self.url,
                    {'name': f"Student {i}", 'phone': f"+998 90 111 22 3{i}"},
                    REMOTE_ADDR='192.168.1.100',
                    HTTP_HOST='127.0.0.1'
                )
                self.assertEqual(resp.status_code, 200, f"Submission {i+1} failed with status {resp.status_code}")

            # 6th submission from the same IP must return 429
            resp_6 = self.client.post(
                self.url,
                {'name': "Student 6", 'phone': "+998 90 111 22 36"},
                REMOTE_ADDR='192.168.1.100',
                HTTP_HOST='127.0.0.1'
            )
            self.assertEqual(resp_6.status_code, 429)
            self.assertFalse(resp_6.json().get('ok'))

        # Only 5 applications should be stored
        self.assertEqual(Application.objects.count(), 5)

    def test_get_not_allowed(self):
        response = self.client.get(self.url, HTTP_HOST='127.0.0.1')
        self.assertEqual(response.status_code, 405)
