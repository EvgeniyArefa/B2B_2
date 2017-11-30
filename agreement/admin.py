import datetime
from django.contrib import admin
from agreement.models import Period, Country, Company, Negotiator, Agreement
from django import forms


class AgreementForm(forms.ModelForm):

    def clean(self):
        # Verification: the start date must be no later than the end date
        start_date = self.cleaned_data.get('data_start')
        end_date = self.cleaned_data.get('data_end')
        if start_date > end_date:
            raise forms.ValidationError\
                ("The end date must be later than the start date")
        return self.cleaned_data


class PeriodForm(forms.ModelForm):

    def clean(self):
        # Verification: the start date must be no later than the end date
        start_date = self.cleaned_data.get('data_start')
        end_date = self.cleaned_data.get('data_end')
        if start_date > end_date:
            raise forms.ValidationError\
                ("The end date must be later than the start date")
        
        # Verification: the dates of the period should not exceed the dates
        # of the agreement
        agreement = self.cleaned_data.get('agreement')
        agr_str = str(agreement)
        if datetime.datetime.strptime(agr_str[0:10], '%Y-%m-%d')\
                .date() > start_date:
            raise forms.ValidationError("The beginning of the period must"+
                " be after the start of the agreement")
        if datetime.datetime.strptime(agr_str[11:21], '%Y-%m-%d')\
                .date() < end_date:
            raise forms.ValidationError("The end of the period must be"+
                " before the end of the agreement")
        
        # Verification: the dates of periods should not overlap with each 
        # other in one agreement
        agr_str_id = agr_str[22:]
        agr_id = ""
        for char in agr_str_id:
            if char == "/":
                break
            else:
                agr_id +=char
        select_periods = Period.objects.filter(agreement__id = int(agr_id))
        for i in range(len(select_periods)):
            period = str(select_periods[i])
            select_start_date = datetime.datetime.strptime(period[0:10], 
                '%Y-%m-%d').date()
            select_end_date = datetime.datetime.strptime(period[11:21], 
                '%Y-%m-%d').date()
            if not (end_date < select_start_date or start_date > \
                select_end_date):
                raise forms.ValidationError("Overlapping periods in one"+\
                    " agreement")
        return self.cleaned_data


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    list_filter = ['name', 'code']
    search_fields = ['name', 'code']


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    list_filter = ['name', 'country']
    search_fields = ['name', 'country']


class NegotiatorAdmin(admin.ModelAdmin):
    list_filter = ['name']
    search_fields = ['name']


class PeriodAdmin(admin.ModelAdmin):
    form = PeriodForm
    list_display = ('status', 'agreement', 'data_start', 'data_end')
    list_filter = ['status', 'agreement','data_start', 'data_end']
    search_fields = ['status', 'agreement']
    date_hierarchy = 'data_end'


class PeriodInline(admin.TabularInline):
    model = Period


class AgreementAdmin(admin.ModelAdmin):
    form = AgreementForm
    inlines = [
        PeriodInline,
    ]
    list_display = ('company', 'data_start', 'data_end', 'negotiator', 
        'loan_turnover', 'debit_turnover_import', 'debit_turnover_export')
    list_filter = ['company', 'data_start', 'data_end','negotiator']
    search_fields = ['company', 'negotiator']
    date_hierarchy = 'data_end'


admin.site.register(Period, PeriodAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Negotiator, NegotiatorAdmin)
admin.site.register(Agreement, AgreementAdmin)