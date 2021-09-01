from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from collection.models import Collection
from collection.serializers import CollectionSerializer


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
        playlist = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = CollectionSerializer(playlist, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
