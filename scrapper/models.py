from django.db import models


class Place(models.Model):
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=35, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()


class Group(models.Model):
    name = models.CharField(max_length=50)
    places = models.ManyToManyField(Place, related_name='groups', blank=True)
