from django.shortcuts import render
from .models import Agreement, Period
from django.http import JsonResponse
from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = 'agreement/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['page_header'] = 'Home page title B2B'
        return context


def calendar(request, country=0, negotiator=0, company=0):
    answer = dict()
    agreements_all = Agreement.objects.all().only('id')

    try:
        if 'country' in request.GET:
            country = (request.GET['country']).split(',')
            agreements_all = agreements_all.filter(company__country__in=
                country).only('id')
        if 'negotiator' in request.GET:
            negotiator = (request.GET['negotiator']).split(',')
            agreements_all = agreements_all.filter(negotiator__id__in=
                negotiator).only('id')
        if 'company' in request.GET:
            company = (request.GET['company']).split(',')
            agreements_all = agreements_all.filter(company__id__in=
                company).only('id')
    except ValueError:
        context = {
            'mes_er': 'You made a mistake when entering the code',
        }
        return render(request, 'agreement/mistake.html', context)

    sel_periods = list(Period.objects.filter(agreement__id__in=
        agreements_all))
    select = 0
    mas_year = 0
    mas_month = 0
    for select_period in sel_periods:
        mass = str(select_period)
        if int(mass[22:]) != select:
            select = int(mass[22:])
            year = answer.get(mas_year, 0)
            if mas_year:
                if not year:
                    answer[mas_year] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                monthes = answer[mas_year]
                monthes[mas_month-1] += 1
                answer[mas_year] = monthes
            mas_year = 0
            mas_month = 0
        if int(mass[11:15]) > mas_year:
            mas_year = int(mass[11:15])
        if int(mass[16:18]) > mas_month:
            mas_month = int(mass[16:18])
    year = answer.get(mas_year, 0)
    if mas_year:
        if not year:
            answer[mas_year] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        monthes = answer[mas_year]
        monthes[mas_month-1] += 1
        answer[mas_year] = monthes

    return JsonResponse(answer, safe=False)
