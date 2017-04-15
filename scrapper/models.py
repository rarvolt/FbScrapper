from django.db import models


class Place(models.Model):
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=35, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return "{}, {}, [{}, {}]".format(self.city, self.country, self.latitude, self.longitude)
