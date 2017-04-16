from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from scrapper.models import Place, Group
from scrapper.serializers import PlaceSerializer, GroupSerializer


@api_view(['GET', 'POST'])
def places_list(request):
    """
    List all places or create new place.
    """
    if request.method == 'GET':
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def place_detail(request, pk):
    """
    Perform operations on single object.
    """
    try:
        place = Place.objects.get(pk=pk)
    except Place.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlaceSerializer(place)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PlaceSerializer(place, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        place.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def groups_list(request):
    """
    List all groups or create new group. 
    """
    if request.method == 'GET':
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def group_detail(request, pk):
    """
    Get, update or delete single group object. 
    """
    try:
        group = Group.objects.get(pk=pk)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Get group details
    if request.method == 'GET':
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    # Update group
    elif request.method == 'PUT':
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete group
    elif request.method == 'DELETE':
        # Exclude places that belong to other groups
        places = group.places.exclude(groups__pk__lt=group.pk).exclude(groups__pk__gt=group.pk)
        places.delete()
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'DELETE'])
def group_places(request, pk):
    try:
        group = Group.objects.get(pk=pk)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Get places in group
    if request.method == 'GET':
        serializer = PlaceSerializer(group.places.all(), many=True)
        return Response(serializer.data)

    # Add places to group
    elif request.method == 'POST':
        places = Place.objects.filter(pk__in=request.data['places'])
        group.places.add(*places)
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    # Delete places from group
    elif request.method == 'DELETE':
        places = group.places.filter(pk__in=request.data['places'])
        group.places.remove(*places)
        serializer = GroupSerializer(group)
        return Response(serializer.data)
