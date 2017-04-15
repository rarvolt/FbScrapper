from django.conf.urls import url

from scrapper import views

urlpatterns = [
    url(r'^places/$', views.place_list, name='places-list'),
    url(r'^places/(?P<pk>[0-9]+)$', views.place_detail, name='place-detail')
]