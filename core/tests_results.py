"""Tests for Results carousel student name display on every card (FIX G)."""
import io
import shutil
import tempfile
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from core.models import Result


class ResultsCardTests(TestCase):
    """Verify that student name is rendered on all result cards."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.temp_media = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_media, ignore_errors=True)
        super().tearDownClass()

    def test_result_with_image_shows_student_name(self):
        """A Result with an image renders the student name in the results section."""
        with override_settings(MEDIA_ROOT=self.temp_media):
            # Create a tiny 10x10 in-memory image
            file_obj = io.BytesIO()
            img = Image.new('RGB', (10, 10), color='green')
            img.save(file_obj, format='JPEG')
            file_obj.seek(0)
            uploaded_image = SimpleUploadedFile(
                'test_score.jpg',
                file_obj.read(),
                content_type='image/jpeg'
            )

            Result.objects.create(
                student_name='Test Student',
                score='1500',
                image=uploaded_image,
                is_active=True,
            )

            response = self.client.get('/uz/')
            self.assertEqual(response.status_code, 200)
            html = response.content.decode()

            self.assertIn('id="results"', html)
            results_section = html.split('id="results"')[1].split('</section>')[0]
            self.assertIn('Test Student', results_section)
            self.assertIn('1500', results_section)
            self.assertIn('OFFICIAL RESULT', results_section)

    def test_result_without_image_shows_student_name(self):
        """A Result without an image renders the student name in the results section."""
        Result.objects.create(
            student_name='No Image Student',
            score='1550',
            image='',
            is_active=True,
        )

        response = self.client.get('/uz/')
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()

        self.assertIn('id="results"', html)
        results_section = html.split('id="results"')[1].split('</section>')[0]
        self.assertIn('No Image Student', results_section)
        self.assertIn('1550', results_section)
        self.assertIn('OFFICIAL RESULT', results_section)

    def test_result_empty_student_name_shows_no_none_or_empty_tag(self):
        """A Result with empty student_name does not output 'None' or an empty student name element."""
        Result.objects.create(
            student_name='',
            score='1480',
            image='',
            is_active=True,
        )

        response = self.client.get('/uz/')
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()

        self.assertIn('id="results"', html)
        results_section = html.split('id="results"')[1].split('</section>')[0]
        self.assertIn('1480', results_section)
        self.assertNotIn('None', results_section)
