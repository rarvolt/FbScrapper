from rest_framework import serializers

from scrapper.models import Place, Group


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('id', 'city', 'country', 'latitude', 'longitude')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'places')
