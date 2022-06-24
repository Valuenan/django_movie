from django.test import TestCase
from django.core.management import call_command


class PositiveLogicTests(TestCase):
    def setUp(self):
        # Load fixtures
        call_command('loaddata', '../fixtures/data.json', verbosity=0)

    def test_genre_filter(self):
        response = self.client.get('/filter/?genre=4')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Анчартед: На картах не значится (2022)')

    def test_genre_filter(self):
        response = self.client.get('/filter/?year=2021')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Главный герой')

    def test_genre_and_year_filters(self):
        response = self.client.get('/filter/?genre=6&genre=5&year=2021')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Главный герой')

    def test_search_first_capitalise(self):
        response = self.client.get('/search/?q=Дю')
        self.assertContains(response, 'Дюна (фильм, 2021)')

    def test_search_firs_lower(self):
        response = self.client.get('/search/?q=дю')
        self.assertContains(response, 'Дюна (фильм, 2021)')

    def test_search_center_part(self):
        response = self.client.get('/search/?q=2021')
        self.assertContains(response, 'Дюна (фильм, 2021)')


class NegativeLogicTests(TestCase):
    def setUp(self):
        # Load fixtures
        call_command('loaddata', '../fixtures/data.json', verbosity=0)

    def test_genre_filter(self):
        response = self.client.get('/filter/?year=2023')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response,
                               ['Главный герой', 'Анчартед: На картах не значится (2022)', 'Дюна (фильм, 2021)'])


