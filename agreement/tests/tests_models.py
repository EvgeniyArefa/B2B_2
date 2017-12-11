from django.test import TestCase
from agreement.models import Period, Country, Company, Negotiator, Agreement
from django.contrib.auth.models import User


class ModelTest(TestCase):

    fixtures = ['D:/Python/Projects/Django/Work/B2B_2/fixtures/data.json']

    def test_neg__str__(self):
        neg = Negotiator.objects.get(id=1)
        self.assertEquals(neg.__str__(), 'user_a')

    def test_country__str__(self):
        country = Country.objects.get(id=1)
        self.assertEquals(country.__str__(), 'Australia')

    def test_company__str__(self):
        company = Company.objects.get(id=1)
        self.assertEquals(company.__str__(), 'AusAirLine')

    def test_period__str__(self):
        period = Period.objects.get(id=1)
        self.assertEquals(period.__str__(), '2017-01-29/2017-11-29/1')
