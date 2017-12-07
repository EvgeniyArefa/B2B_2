from django.test import TestCase
from agreement.models import Period, Country, Company, Negotiator, Agreement
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class MainTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            password='qwertyuiop', username='a', first_name='A',
            last_name='a', email='a@.net', id=1
            )
        neg = Negotiator.objects.create(name=user)
        country = Country.objects.create(name='Zambia', code='ZMB', id=1)
        company = Company.objects.create(name='Kukh', country=country, id=1)
        agreement = Agreement.objects.create(
            data_start='2017-01-01', data_end='2017-12-31', company=company,
            negotiator=neg, loan_turnover=0, debit_turnover=0, id=1
            )
        Period.objects.create(
            data_start='2017-02-01', data_end='2017-03-01',
            status=1, agreement=agreement, id=1
            )

    def test_calendar_url_exists(self):
        request = self.client.get('/agreements/calendar/')
        self.assertEqual(request.status_code, 200)

    def test_HomeView_url_exists(self):
        request = self.client.get('/home/')
        self.assertEqual(request.status_code, 200)

    def test_HomeView_page_header_exists(self):
        resp = self.client.get(reverse('home'))
        self.assertTrue('page_header' in resp.context)
