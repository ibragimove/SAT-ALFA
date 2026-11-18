from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from core.models import SiteSettings, Application


class AdminChangelistTests(TestCase):
    def setUp(self):
        self.username = 'admin'
        self.password = 'AdminPassword123!'
        self.superuser = User.objects.create_superuser(
            username=self.username,
            email='admin@sat-alfa.uz',
            password=self.password,
        )
        self.client = Client()
        logged_in = self.client.login(username=self.username, password=self.password)
        self.assertTrue(logged_in, "Superuser login failed.")

    def test_changelists_http_200(self):
        models = [
            'textblock',
            'sitesettings',
            'stat',
            'advantage',
            'teacher',
            'tariffplan',
            'result',
            'event',
            'faq',
            'application',
        ]
        for model in models:
            url = reverse(f'admin:core_{model}_changelist')
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                200,
                f"Failed to load changelist for {model}: status {response.status_code}",
            )

    def test_sitesettings_singleton_rules(self):
        add_url = reverse('admin:core_sitesettings_add')
        # When 0 rows exist, add page is accessible
        response = self.client.get(add_url)
        self.assertEqual(response.status_code, 200)

        # Create one row
        settings_obj = SiteSettings.objects.create(
            phone='+998901234567',
            hero_title='SAT ALFA',
            address='Tashkent',
            working_hours='09:00 - 20:00'
        )

        # When 1 row exists, add is not allowed (redirect or 403)
        response = self.client.get(add_url)
        self.assertIn(response.status_code, [302, 403])

        # Delete is not allowed
        delete_url = reverse('admin:core_sitesettings_delete', args=[settings_obj.pk])
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 403)

    def test_application_readonly_rules(self):
        add_url = reverse('admin:core_application_add')
        response = self.client.get(add_url)
        self.assertEqual(response.status_code, 403)

        app = Application.objects.create(name='Test User', phone='+998901234567')
        change_url = reverse('admin:core_application_change', args=[app.pk])
        response = self.client.get(change_url)
        # View permission is granted, so change page renders read-only
        self.assertEqual(response.status_code, 200)
        # Verify submit button is not present
        self.assertNotContains(response, 'name="_save"')
