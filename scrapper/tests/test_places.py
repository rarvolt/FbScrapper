from django.test import TestCase

from scrapper.models import Place


class PlaceModelTest(TestCase):
    def test_can_save_and_retreive_place(self):
        place = Place(
            city='Poznan',
            country='Poland',
            latitude=52.6,
            longitude=16.9167
        )
        place.save()

        saved_place = Place.objects.get()

        self.assertEqual(Place.objects.count(), 1)
        self.assertEqual(place, saved_place)

    def test_model_repr(self):
        place = Place(
            city='Poznan',
            country='Poland',
            latitude=52.6,
            longitude=16.9167
        )
        self.assertEqual(place.__str__(), "Poznan, Poland, [52.6, 16.9167]")
