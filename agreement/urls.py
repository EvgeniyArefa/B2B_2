from django.conf.urls import url
from . import views
from agreement.views import HomeView


urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^home/$', HomeView.as_view(), name='home'),
    url(r'^agreements/calendar/(?:\?country=(?P<country>.+))?$',
        views.calendar, name='calendar'),
]
