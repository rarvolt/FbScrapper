from rest_framework import serializers

from scrapper.models import Place


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('id', 'city', 'country', 'latitude', 'longitude')
