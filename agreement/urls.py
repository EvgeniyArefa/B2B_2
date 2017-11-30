from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name = "home"),
    url(r'^home/$', views.home, name = "home"),
    url(r'^agreements/calendar/(?:\?country=(?P<country>.+))?$',\
        views.calendar, name = "calendar"),
]