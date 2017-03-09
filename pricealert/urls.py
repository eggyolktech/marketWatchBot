from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^filter/(?P<symbol_filter>\w{1,50})/$', views.filter, name='filter'),
]