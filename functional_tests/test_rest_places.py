import json
from collections import OrderedDict

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from scrapper.models import Place


class AddNewPlaceTest(APITestCase):
    def test_can_add_new_place(self):
        """
        Test if we can add new place to database.
        """
        url = reverse('places-list')
        new_place_data = {
            'city': 'Berlin',
            'country': 'Germany',
            'latitude': 52.514355,
            'longitude': 13.405883
        }

        response = self.client.post(url, new_place_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Place.objects.count(), 1)
        self.assertEqual(Place.objects.get().city, 'Berlin')
        self.assertEqual(Place.objects.get().country, 'Germany')
        self.assertEqual(Place.objects.get().latitude, 52.514355)
        self.assertEqual(Place.objects.get().longitude, 13.405883)

    def test_required_fields(self):
        """
        Test if can add place without optional fields
        and cannot withoit required ones
        """
        url = reverse('places-list')
        test_optional_data = {
            'latitude': 52.514355,
            'longitude': 13.405883
        }
        test_required_data = {
            'city': 'Berlin',
            'country': 'Germany',
            'longitude': 13.405883
        }

        response = self.client.post(url, test_optional_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Place.objects.count(), 1)

        response = self.client.post(url, test_required_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Place.objects.count(), 1)

    def test_data_is_validated(self):
        """
        Test if data is validated before saving and error is returned if not valid.
        """
        url = reverse('places-list')
        bad_place_data = {
            'city': 'Berlin',
            'country': 'Germany',
            'latitude': 'not_a_number',
            'longitude': 13.405883
        }

        response = self.client.post(url, bad_place_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Place.objects.count(), 0)


class GetPlacesTest(APITestCase):
    def test_get_all_places(self):
        """
        Test if can retrieve all places.
        """
        url = reverse('places-list')

        Place(city='Warsaw', country='Poland', latitude=52.25, longitude=21).save()
        Place(city='Berlin', country='Germany', latitude=52.516, longitude=13.4059).save()

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn({
            'id': 1,
            'city': 'Warsaw',
            'country': 'Poland',
            'latitude': 52.25,
            'longitude': 21
        }, response.data)
        self.assertIn({
            'id': 2,
            'city': 'Berlin',
            'country': 'Germany',
            'latitude': 52.516,
            'longitude': 13.4059
        }, response.data)

    def test_get_place(self):
        """
        Test if can retrieve single place by id.
        """
        place = Place(city='Warsaw', country='Poland', latitude=52.25, longitude=21)
        place.save()
        url = reverse('place-detail', kwargs={'pk': place.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': 1,
            'city': 'Warsaw',
            'country': 'Poland',
            'latitude': 52.25,
            'longitude': 21
        })

    def test_get_place_not_found(self):
        """
        Test for apropriate error if requested place does not exist 
        """
        url = reverse('place-detail', kwargs={'pk': 1})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdatePlaceTest(APITestCase):
    def test_update_place(self):
        """
        Test if can update place fields. 
        """
        place = Place(city='Warsaw', country='Poland', latitude=52.25, longitude=21)
        place.save()
        url = reverse('place-detail', kwargs={'pk': place.id})
        updated_place_data = {
            'city': 'Berlin',
            'country': 'Germany',
            'latitude': 52.516,
            'longitude': 13.4059
        }

        response = self.client.put(url, updated_place_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Place.objects.get().city, 'Berlin')
        self.assertEqual(Place.objects.get().country, 'Germany')
        self.assertEqual(Place.objects.get().latitude, 52.516)
        self.assertEqual(Place.objects.get().longitude, 13.4059)

    def test_bad_update_place(self):
        """
        Test if place is validated before updating.
        """
        place = Place(city='Warsaw', country='Poland', latitude=52.25, longitude=21)
        place.save()
        url = reverse('place-detail', kwargs={'pk': place.id})
        bad_place_data = {
            'city': 'Berlin',
            'country': 'Germany',
            'latitude': 'not_a_number',
            'longitude': 13.405883
        }

        response = self.client.put(url, bad_place_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(place, Place.objects.get())

    def test_update_place_not_found(self):
        """
        Test for apropriate error if requested place does not exist 
        """
        url = reverse('place-detail', kwargs={'pk': 1})
        updated_place_data = {
            'city': 'Berlin',
            'country': 'Germany',
            'latitude': 52.516,
            'longitude': 13.4059
        }

        response = self.client.put(url, updated_place_data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Place.objects.count(), 0)


class DeletePlaceTest(APITestCase):
    def test_delete_place(self):
        """
        Test if can delete existing place 
        """
        place = Place(city='Warsaw', country='Poland', latitude=52.25, longitude=21)
        place.save()
        url = reverse('place-detail', kwargs={'pk': place.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Place.objects.count(), 0)

    def test_delete_place_not_found(self):
        """
        Test for apropriate error if requested place does not exist 
        """
        url = reverse('place-detail', kwargs={'pk': 1})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
