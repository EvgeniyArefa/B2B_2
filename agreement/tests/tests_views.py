from django.test import TestCase
from django.core.urlresolvers import reverse


class MainTests(TestCase):

    fixtures = ['D:/Python/Projects/Django/Work/B2B_2/fixtures/data.json']

    def test_calendar_url_exists(self):
        request = self.client.get('/agreements/calendar/')
        self.assertEqual(request.status_code, 200)

    def test_HomeView_url_exists(self):
        request = self.client.get('/home/')
        self.assertEqual(request.status_code, 200)

    def test_HomeView_page_header_exists(self):
        resp = self.client.get(reverse('home'))
        self.assertTrue('page_header' in resp.context)
