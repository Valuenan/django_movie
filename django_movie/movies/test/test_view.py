from django.test import TestCase
from django.core.management import call_command


class PositiveViewTests(TestCase):
    def setUp(self):
        # Load fixtures
        call_command('loaddata', '../fixtures/data.json', verbosity=0)

    def test_index(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/movie_list.html')

    def test_movie(self):
        response = self.client.get('/movie/dune_2021/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/movie_detail.html')

    def test_actor(self):
        response = self.client.get('/actor/Джейсон%20Момоа/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/actor.html')


class NegativeViewTests(TestCase):
    def setUp(self):
        # Load fixtures
        call_command('loaddata', '../fixtures/data.json', verbosity=0)

    def test_movie(self):
        response = self.client.get('/movie/test/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.context['exception'], 'Не найден ни один Фильм, соответствующий запросу')

    def test_actor(self):
        response = self.client.get('/actor/Test/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.context['exception'], 'Не найден ни один Актеры и режисеры, соответствующий запросу')
