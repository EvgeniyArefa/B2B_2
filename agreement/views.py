import datetime
from django.shortcuts import render
from .models import Agreement, Period
import json
from django.http import HttpResponse


# Function of separation ID
# Returns a single identifier without a comma
# Returns "None", if not number or 0
def separation(set_in):
    double_comma = 0
    result = []
    set_path = ""
    for char in str(set_in):
        if char == ",":
            double_comma += 1
            if double_comma > 1:
                return None
            if set_path:
                try:
                    result.append(int(set_path))
                except ValueError:
                    return None
                set_path = ""
        elif char == "0" or char == "-":
            return None
        else:
            set_path +=char
            double_comma = 0
    try:
        result.append(int(set_path))
    except ValueError:
        return None  
    return result


def home(request):
    context ={
        'page_header': 'Home page title B2B',
    }
    return render(request, 'agreement/home.html', context)


def calendar(request, country=0, negotiator=0, company=0):
    answer = dict()
    # Getting and validation ones ID
    if 'country' in request.GET:
        country = request.GET['country']
        country = separation(country)
        if country == None:
            context = {
                'mes_er':"You made a mistake when entering the country code",
            }
            return render(request, 'agreement/mistake.html', context)
    if 'negotiator' in request.GET:
        negotiator = request.GET['negotiator']
        negotiator = separation(negotiator)
        if negotiator == None:
            context = {
                'mes_er':"You made a mistake when entering the negotiator",
            }
            return render(request, 'agreement/mistake.html', context)
    if 'company' in request.GET:
        company = request.GET['company']
        company = separation(company)
        if company == None:
            context = {
                'mes_er':"You made a mistake when entering the company code",
            }
            return render(request, 'agreement/mistake.html', context)
    if not country:
        country = 0
    
    # Filter definition
    if country == 0:
        if negotiator == 0:
            if company == 0:
                agreements_all = Agreement.objects.all()
            else:
                agreements_all = Agreement.objects.filter\
                    (company__id__in=company)
        else:
            if company == 0:
                agreements_all = Agreement.objects.filter\
                    (negotiator__id__in=negotiator)
            else:
                agreements_all = Agreement.objects.filter\
                    (company__id__in=company, negotiator__id__in=negotiator)
    else:
        if negotiator == 0:
            if company == 0:
                agreements_all = Agreement.objects.filter\
                    (company__country__in=country)
            else:
                agreements_all = Agreement.objects.filter\
                    (company__country__in=country, company__id__in=company)
        else:
            if company == 0:
                agreements_all = Agreement.objects.filter\
                    (company__country__in=country, negotiator__id__in=\
                        negotiator)
            else:
                agreements_all = Agreement.objects.filter\
                    (company__country__in=country, company__id__in=company,\
                    negotiator__id__in=negotiator)      
    if not agreements_all:
        context = {
        'mes_er': "Your sample is empty",
        }
        return render(request, 'agreement/mistake.html', context)
    
    for select_agreement in agreements_all:
        id_agr = int(select_agreement.id)
        select_periods = Period.objects.filter(agreement__id=id_agr)
        mas_year = 0
        mas_month = 0
        for i in range(len(select_periods)):
            mass = str(select_periods[i])
            if int(mass[11:15]) > mas_year:
                mas_year = int(mass[11:15])
            if int(mass[16:18]) > mas_month:
                mas_month = int(mass[16:18])
        year = answer.get(mas_year, 0)
        if mas_year:
            if not year:
                answer[mas_year] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            monthes = answer[mas_year]
            monthes[mas_month-1] +=1
            answer[mas_year] = monthes
    return HttpResponse(json.dumps(answer), content_type='application/json')