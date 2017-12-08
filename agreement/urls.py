from django.conf.urls import url
from agreement.views import HomeView, CaledarView


urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^home/$', HomeView.as_view(), name='home'),
    url(r'^agreements/calendar/(?:\?country=(?P<country>.+))?$',
        CaledarView.as_view(), name='calendar'),
]
