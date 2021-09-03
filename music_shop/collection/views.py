from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from collection.models import Collection
from collection.serializers import CollectionSerializer
from song.models import Song


class CollectionViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        serializer = CollectionSerializer(
            self.get_queryset(), many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        collection = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = CollectionSerializer(collection, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["delete"])
    def unlike(self, request, pk=None, song_id=None):
        collection = get_object_or_404(self.get_queryset(), pk=pk)
        song = get_object_or_404(Song, pk=song_id)
        if collection.song.all().filter(id=song.id).exists():
            collection.song.remove(song)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                "There is no such a song in your collection!",
                status=status.HTTP_404_NOT_FOUND,
            )
