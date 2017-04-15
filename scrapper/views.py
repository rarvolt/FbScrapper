from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from scrapper.models import Place
from scrapper.serializers import PlaceSerializer


@api_view(['GET', 'POST'])
def place_list(request):
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
