import re

from django.test import TestCase, override_settings
from django.urls import reverse

from .models import AcademicProgram, AdmissionApplication


@override_settings(STORAGES={
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
})
class AdmissionApplicationTests(TestCase):
    def setUp(self):
        self.program = AcademicProgram.objects.create(
            name='Diploma in Computer Science',
            level='diploma',
            duration='2 Years',
            is_active=True,
        )

    def create_application(self, **overrides):
        data = {
            'program': self.program,
            'applicant_name': 'Ali Khan',
            'father_name': 'Khan Muhammad',
            'cnic_or_bform': '12345-1234567-1',
            'phone': '03001234567',
            'email': 'ali@example.com',
            'address': 'D.I. Khan',
            'obtained_marks': 880,
            'total_marks': 1100,
        }
        data.update(overrides)
        return AdmissionApplication.objects.create(**data)

    def test_application_number_uses_unique_mixed_gcms_code(self):
        application = self.create_application()

        self.assertRegex(application.application_number, r'^GCMS-[2-9A-Z]{4}-[2-9A-Z]{4}$')
        self.assertIsNone(re.match(r'^GCMS-\d{8}-\d{4}$', application.application_number))
        self.assertFalse(application.application_number.startswith('GCMS-ADM-'))

    def test_status_post_redirects_to_search_result_url(self):
        application = self.create_application()

        response = self.client.post(reverse('admission_status'), {
            'application_number': application.application_number.lower(),
        })

        self.assertRedirects(
            response,
            f"{reverse('admission_status')}?application_number={application.application_number.lower()}",
            fetch_redirect_response=False,
        )

    def test_status_page_shows_application_details_and_print_button(self):
        application = self.create_application(status='confirmed', admin_notes='Bring original documents.')

        response = self.client.get(reverse('admission_status'), {
            'application_number': application.application_number,
        })

        self.assertContains(response, application.application_number)
        self.assertContains(response, 'Ali Khan')
        self.assertContains(response, 'Diploma in Computer Science')
        self.assertContains(response, 'Confirmed')
        self.assertContains(response, 'Bring original documents.')
        self.assertContains(response, 'img/gcms-logo.jpeg')
        self.assertContains(response, 'Admissions Office Signature')
        self.assertContains(response, 'window.print()')
