from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from album.models import Album
from album.serializers import AlbumSerializer
from song.serializers import SongSerializerGet


class AlbumViewSet(ViewSet):
    def list(self, request, *args, **kwargs):
        queryset = Album.objects.all()
        serializer = AlbumSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = Album.objects.all()
        album = get_object_or_404(queryset, pk=pk)
        serializer = AlbumSerializer(album)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = AlbumSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        queryset = Album.objects.filter(pk=pk)

        if queryset:
            serializer = AlbumSerializer(queryset.first(), data=request.data)
        else:
            serializer = AlbumSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if queryset:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        queryset = Album.objects.all()
        album = get_object_or_404(queryset, pk=pk)
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get"])
    def songs(self, request, pk=None):
        album = get_object_or_404(Album, pk=pk)
        album_songs = album.album.all()
        serializer = SongSerializerGet(
            album_songs, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
