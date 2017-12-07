from django.test import TestCase
from agreement.models import Period, Country, Company, Negotiator, Agreement
from django.contrib.auth.models import User


class ModelTest(TestCase):

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
            data_start='2017-02-01', data_end='2017-03-01', status=1,
            agreement=agreement, id=1
            )

    def test_neg__str__(self):
        neg = Negotiator.objects.get()
        self.assertEquals(neg.__str__(), 'a')

    def test_country__str__(self):
        country = Country.objects.get()
        self.assertEquals(country.__str__(), 'Zambia')

    def test_company__str__(self):
        company = Company.objects.get()
        self.assertEquals(company.__str__(), 'Kukh')

    def test_period__str__(self):
        period = Period.objects.get()
        self.assertEquals(period.__str__(), '2017-02-01/2017-03-01/1')
