from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from scrapper.models import Group, Place


class AddNewGroupTest(APITestCase):
    def test_can_add_new_empty_group(self):
        """
        Test if can add new empty group do database 
        """
        url = reverse('groups-list')
        new_group_data = {'name': 'test_grp'}

        response = self.client.post(url, new_group_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(Group.objects.get().name, 'test_grp')

    def test_can_add_new_group_with_places(self):
        """
        Test if can add new group with existing places 
        """
        place1 = Place(city='Warsaw', country='Poland', latitude=52.25, longitude=21)
        place1.save()
        place2 = Place(city='Berlin', country='Germany', latitude=52.516, longitude=13.4059)
        place2.save()

        url = reverse('groups-list')
        new_group_data = {
            'name': 'test_grp',
            'places': [place1.id, place2.id]
        }

        response = self.client.post(url, new_group_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        places = Group.objects.get().places.all()
        self.assertEqual(places.count(), 2)
        self.assertIn(place1, places)
        self.assertIn(place2, places)

    def test_empty_name_validation(self):
        """
        Test for error messages on bad data 
        """
        url = reverse('groups-list')
        bad_group_data = {'name': ''}

        response = self.client.post(url, bad_group_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Group.objects.count(), 0)

    def test_add_new_group_with_nonexistent_place(self):
        """
        Test for error messages on adding new group with place thas doesn't exist 
        """
        url = reverse('groups-list')
        bad_group_data = {'name': 'test_grp', 'places': [1]}

        response = self.client.post(url, bad_group_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Group.objects.count(), 0)


class GetGroupsTest(APITestCase):
    def test_get_all_groups(self):
        """
        Test if can retrieve all groups
        """
        place1 = Place(city='Warsaw', country='Poland', latitude=52.25, longitude=21)
        place1.save()
        place2 = Place(city='Berlin', country='Germany', latitude=52.516, longitude=13.4059)
        place2.save()

        group1 = Group(name='grp1')
        group1.save()
        group1.places.add(place1)

        group2 = Group(name='grp2')
        group2.save()
        group2.places.add(place1, place2)

        url = reverse('groups-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn({
            'id': 1,
            'name': 'grp1',
            'places': [1]
        }, response.data)
        self.assertIn({
            'id': 2,
            'name': 'grp2',
            'places': [1, 2]
        }, response.data)

    def test_get_group(self):
        """
        Test if can retrieve single group by id 
        """
        place1 = Place(city='Warsaw', country='Poland', latitude=52.25, longitude=21)
        place1.save()
        group1 = Group(name='grp1')
        group1.save()
        group1.places.add(place1)

        url = reverse('group-detail', kwargs={'pk': group1.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({
            'id': 1,
            'name': 'grp1',
            'places': [1]
        }, response.data)

    def test_group_not_found(self):
        """
        Test for appropriate error if group does not exist 
        """
        url = reverse('group-detail', kwargs={'pk': 1})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateGroupTest(APITestCase):
    def test_update_group_name(self):
        """
        Test if can update group name 
        """
        group = Group.objects.create(name='grp1')
        url = reverse('group-detail', kwargs={'pk': group.id})
        updated_group_data = {
            'name': 'grp12'
        }

        response = self.client.put(url, updated_group_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Group.objects.get().name, 'grp12')

    def test_update_group_places(self):
        """
        Test if can update group's places list 
        """
        group = Group.objects.create(name='grp1')
        place1 = Place.objects.create(city='Warsaw', country='Poland', latitude=52.25, longitude=21)
        place2 = Place.objects.create(city='Berlin', country='Germany', latitude=52.516, longitude=13.4059)
        group.places.add(place1)

        url = reverse('group-detail', kwargs={'pk': group.id})
        updated_group_data = {
            'name': 'grp2',
            'places': [place2.id]
        }

        response = self.client.put(url, updated_group_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Group.objects.get().places.get(), place2)

    def test_bad_update_group_name(self):
        """
        Test if group is validated before updating 
        """
        group = Group.objects.create(name='grp1')
        url = reverse('group-detail', kwargs={'pk': group.id})
        bad_group_data = {
            'name': ''
        }

        response = self.client.put(url, bad_group_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Group.objects.get().name, 'grp1')

    def test_update_group_not_found(self):
        """
        Test for appropriate error if requested group does not exist
        """
        url = reverse('group-detail', kwargs={'pk': 1})
        updated_group_data = {
            'name': 'grp12'
        }

        response = self.client.put(url, updated_group_data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Group.objects.count(), 0)

    def test_add_group_places(self):
        """
        Test adding places to existing group 
        """
        group = Group.objects.create(name='grp1')
        place1 = Place.objects.create(city='Warsaw', country='Poland', latitude=52.25, longitude=21)
        place2 = Place.objects.create(city='Berlin', country='Germany', latitude=52.516, longitude=13.4059)

        url = reverse('group-places', kwargs={'pk': group.id})
        add_group_places_data = {
            'places': [place1.id, place2.id]
        }

        response = self.client.post(url, add_group_places_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(place1, Group.objects.get().places.all())
        self.assertIn(place2, Group.objects.get().places.all())

    def test_remove_group_places(self):
        """
        Test removing places from existing groups 
        """
        group = Group.objects.create(name='grp1')
        place1 = Place.objects.create(city='Warsaw', country='Poland', latitude=52.25, longitude=21)
        place2 = Place.objects.create(city='Berlin', country='Germany', latitude=52.516, longitude=13.4059)
        group.places.add(place1, place2)

        url = reverse('group-places', kwargs={'pk': group.id})
        remove_group_places_data = {
            'places': [place1.id]
        }

        response = self.client.delete(url, remove_group_places_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(place2, Group.objects.get().places.all())
        self.assertNotIn(place1, Group.objects.get().places.all())

    def test_get_group_places(self):
        """
        Test retrieving places' details from single group 
        """
        group = Group.objects.create(name='grp1')
        place1 = Place.objects.create(city='Warsaw', country='Poland', latitude=52.25, longitude=21)
        place2 = Place.objects.create(city='Berlin', country='Germany', latitude=52.516, longitude=13.4059)
        group.places.add(place1, place2)

        url = reverse('group-places', kwargs={'pk': group.id})

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

    def test_get_nonexistent_group_places(self):
        """
        Test for appropriate error message if requested group does not exist 
        """
        url = reverse('group-places', kwargs={'pk': 1})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteGroupTest(APITestCase):
    def test_delete_empty_group(self):
        """
        Test deleting empty group 
        """
        group = Group.objects.create(name='grp1')

        url = reverse('group-detail', kwargs={'pk': group.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Group.objects.count(), 0)

    def test_delete_nonempty_group(self):
        """
        Test deleting group with places assigned to it
        Assigned places should be deleted
        """
        group = Group.objects.create(name='grp1')
        place1 = Place.objects.create(city='Warsaw', country='Poland', latitude=52.25, longitude=21)
        place2 = Place.objects.create(city='Berlin', country='Germany', latitude=52.516, longitude=13.4059)
        group.places.add(place1, place2)

        url = reverse('group-detail', kwargs={'pk': group.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Group.objects.count(), 0)
        self.assertEqual(Place.objects.count(), 0)

    def test_delete_nonempty_multiple_groups(self):
        """
        Test deleting groups with places assigned to it and other group
        Places belonging to other groups should not be deleted
        """
        group1 = Group.objects.create(name='grp1')
        group2 = Group.objects.create(name='grp2')
        place1 = Place.objects.create(city='Warsaw', country='Poland', latitude=52.25, longitude=21)
        place2 = Place.objects.create(city='Berlin', country='Germany', latitude=52.516, longitude=13.4059)
        group1.places.add(place1, place2)
        group2.places.add(place2)

        url = reverse('group-detail', kwargs={'pk': group1.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(Group.objects.get(), group2)
        self.assertEqual(Place.objects.count(), 1)
        self.assertEqual(Place.objects.get(), place2)
        self.assertEqual(Place.objects.get(), group2.places.get())
