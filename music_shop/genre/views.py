from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from genre.models import Genre
from genre.serializers import GenreSerializer


class GenreViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        queryset = Genre.objects.all()
        serializer = GenreSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = Genre.objects.all()
        playlist = get_object_or_404(queryset, pk=pk)
        serializer = GenreSerializer(playlist, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
