from django.conf.urls import url

from scrapper import views

urlpatterns = [
    url(r'^places/$', views.places_list, name='places-list'),
    url(r'^places/(?P<pk>[0-9]+)$', views.place_detail, name='place-detail'),
    url(r'^groups/$', views.groups_list, name='groups-list'),
    url(r'^groups/(?P<pk>[0-9]+)$', views.group_detail, name='group-detail'),
    url(r'^groups/(?P<pk>[0-9]+)/places/$', views.group_places, name='group-places'),
]
