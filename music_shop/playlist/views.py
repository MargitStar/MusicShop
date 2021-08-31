from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from playlist.models import Playlist
from playlist.serializers import PlaylistSerializer, PlaylistSerializerPost
from playlist.validation import validate_songs


class PlaylistViewSet(ViewSet):
    def list(self, request, *args, **kwargs):
        queryset = Playlist.objects.all()
        serializer = PlaylistSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = Playlist.objects.all()
        playlist = get_object_or_404(queryset, pk=pk)
        serializer = PlaylistSerializer(playlist, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        validate_songs(request)
        serializer = PlaylistSerializerPost(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        queryset = Playlist.objects.filter(pk=kwargs["pk"])
        validate_songs(request)

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

    def destroy(self, request, pk=None):
        user = self.request.user
        queryset = Playlist.objects.all()
        playlist = get_object_or_404(queryset, pk=pk)
        if user == playlist.user:
            playlist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("This is not your playlist")

    def get_permissions(self):
        if self.request.method == "GET" or self.request.method == "OPTIONS":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated,)
        return super(PlaylistViewSet, self).get_permissions()
