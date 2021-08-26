from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from playlist.models import Playlist
from playlist.serializers import PlaylistSerializer, PlaylistSerializerPost


class PlaylistViewSet(ViewSet):
    # permission_classes = (IsAuthenticated,)
    # queryset = Playlist.objects.all()
    # serializer_class = PlaylistSerializer

    def list(self, request, *args, **kwargs):
        queryset = Playlist.objects.all()
        serializer = PlaylistSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = Playlist.objects.all()
        playlist = get_object_or_404(queryset, pk=pk)
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = PlaylistSerializerPost(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        queryset = Playlist.objects.filter(pk=kwargs["pk"])
        if queryset:
            serializer = PlaylistSerializerPost(
                queryset.first(), data=request.data, partial=partial
            )
        else:
            serializer = PlaylistSerializerPost(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        if queryset:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, pk=None):
        queryset = Playlist.objects.all()
        playlist = get_object_or_404(queryset, pk=pk)
        playlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method == "GET" or self.request.method == "OPTIONS":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated,)
        return super(PlaylistViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.request.method == "GET" or self.request.method == "OPTIONS":
            return PlaylistSerializer
        elif self.request.method != "DELETE":
            return PlaylistSerializerPost
