from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from core.models import Participant
from core.utils import normalize_digits


class NormalizeDigitsTests(TestCase):
    def test_arabic_indic_digits(self):
        self.assertEqual(
            normalize_digits('٢٩٥٠١٠١١٢٣٤٥٦٧'),
            '29501011234567',
        )

    def test_mixed_digits(self):
        self.assertEqual(normalize_digits('2950١٠١١٢34567'), '29501011234567')


class SearchTests(TestCase):
    def setUp(self):
        Participant.objects.create(
            participant_id='29501011234567',
            name='أحمد محمد',
            rank=1,
            result='98.50',
        )
        self.client = Client()

    def test_search_with_arabic_digits(self):
        response = self.client.post(
            '/',
            {'participant_id': '٢٩٥٠١٠١١٢٣٤٥٦٧'},
        )
        self.assertRedirects(response, '/result/29501011234567/')

    def test_search_with_western_digits(self):
        response = self.client.post(
            '/',
            {'participant_id': '29501011234567'},
        )
        self.assertRedirects(response, '/result/29501011234567/')


class ManageTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='admin',
            password='testpass123',
            is_staff=True,
        )
        self.client = Client()
        self.client.login(username='admin', password='testpass123')

    def test_dashboard_requires_login(self):
        client = Client()
        response = client.get(reverse('manage_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/manage/login/'))

    def test_add_student(self):
        response = self.client.post(reverse('manage_add'), {
            'name': 'سارة أحمد',
            'participant_id': '28801011234567',
            'result': '91.25',
            'rank': '',
        })
        self.assertRedirects(response, reverse('manage_dashboard'))
        self.assertTrue(Participant.objects.filter(participant_id='28801011234567').exists())

    def test_delete_student(self):
        participant = Participant.objects.create(
            participant_id='27701011234567',
            name='محمد',
            result='88.00',
        )
        response = self.client.post(reverse('manage_delete', args=[participant.pk]))
        self.assertRedirects(response, reverse('manage_dashboard'))
        self.assertFalse(Participant.objects.filter(pk=participant.pk).exists())
