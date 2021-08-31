from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from playlist.models import Playlist
from song.filters import SongFilter
from song.models import BlockedSong, Song, SongData
from song.permissions import ModeratorPermission
from song.serializers import (
    BlockedSongSerializerGet,
    BlockedSongSerializerPost,
    SongDataSerializer,
    SongSerializerGet,
    SongSerializerPost,
)


class SongDataCreateView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = SongDataSerializer
    queryset = SongData.objects.all()


class SongViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        queryset = Song.objects.all()
        fil = SongFilter(request.GET, queryset=queryset)
        serializer = SongSerializerGet(fil.qs, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = Song.objects.all()
        playlist = get_object_or_404(queryset, pk=pk)
        serializer = SongSerializerGet(playlist, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = SongSerializerPost(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        queryset = Song.objects.filter(pk=kwargs["pk"])
        if queryset:
            serializer = SongSerializerPost(
                queryset.first(), data=request.data, partial=partial
            )
        else:
            serializer = SongSerializerPost(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if queryset:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        queryset = Song.objects.all()
        song = get_object_or_404(queryset, pk=pk)
        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.request.method == "GET" or self.request.method == "OPTIONS":
            return SongSerializerGet
        elif self.request.method != "DELETE":
            return SongSerializerPost

    @action(detail=True, methods=["get"])
    def data(self, request, pk=None):
        instance = SongData.objects.get(pk=pk)
        file_handle = instance.data.open()

        response = FileResponse(file_handle, content_type="audio/mpeg")
        response["Content-Length"] = instance.data.size
        response["Content-Disposition"] = (
            'attachment; filename="%s"' % instance.data.name
        )
        return response

    @action(
        detail=True, methods=["get"], permission_classes=(permissions.IsAuthenticated,)
    )
    def playlist(self, request, pk=None, playlist_id=None):
        song = Song.objects.get(pk=pk)
        playlist = Playlist.objects.get(pk=playlist_id)
        if self.request.user == playlist.user:
            playlist.song.add(song)
            playlist.save()
            return Response("Added")
        else:
            return Response("It is not your playlist", status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=["put"], permission_classes=(ModeratorPermission,))
    def blocked(self, request, pk=None):
        song = Song.objects.get(pk=pk)
        user = self.request.user
        blocked_song = BlockedSong.objects.filter(song=song)
        if blocked_song:
            serializer = BlockedSongSerializerPost(
                blocked_song.first(), data=request.data
            )
        else:
            serializer = BlockedSongSerializerPost(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(song=song, user=user)
        if not blocked_song:
            return Response(
                f"{song.title} is in blacklist now!", status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                f"{song.title} is in blacklist now", status=status.HTTP_200_OK
            )


class BlockedSongViewSet(viewsets.ViewSet):
    permission_classes = (ModeratorPermission,)

    def list(self, request, *args, **kwargs):
        queryset = BlockedSong.objects.all()
        serializer = BlockedSongSerializerGet(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = BlockedSong.objects.all()
        blocked_song = get_object_or_404(queryset, pk=pk)
        serializer = BlockedSongSerializerGet(
            blocked_song, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        queryset = BlockedSong.objects.all()
        song = get_object_or_404(queryset, pk=pk)
        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
