from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class Negotiator(models.Model):
    name = models.ForeignKey(User)

    def __str__(self):
        return str(self.name)


class Agreement(models.Model):
    data_start = models.DateField()
    data_end = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    negotiator = models.ForeignKey(Negotiator, on_delete=models.CASCADE)
    loan_turnover = models.FloatField(blank=True, default=0)
    debit_turnover = models.FloatField(blank=True, default=0)

    def __str__(self):
        return (
            str(self.data_start) + '/' + str(self.data_end) + '/' +
            str(self.id) + '/' + str(self.company)
            )


class Period(models.Model):
    choice = ((1, 'New'), (2, 'Active'), (3, 'Reconciliation'), (4, 'Closed'))
    data_start = models.DateField()
    data_end = models.DateField()
    status = models.IntegerField(choices=choice)
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE)

    def __str__(self):
        return (
            str(self.data_start) + '/' + str(self.data_end) + '/' +
            str(self.agreement.id)
            )
