from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from playlist.models import Playlist
from song.models import BlockedSong, Song, SongData
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


class SongViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = (
        "release_date",
        "author__name",
        "author__surname",
        "title",
        "genre__name",
    )
    search_fields = ["^title"]
    queryset = Song.objects.all()

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

    @action(detail=True, methods=["get"])
    def playlist(self, request, pk=None, playlist_id=None):
        song = Song.objects.get(pk=pk)
        playlist = Playlist.objects.get(pk=playlist_id)
        if self.request.user == playlist.user:
            playlist.song.add(song)
            playlist.save()
            return Response("Added")
        else:
            return Response("It is not your playlist", status=status.HTTP_403_FORBIDDEN)

    @action(
        detail=True, methods=["put"], permission_classes=(permissions.IsAuthenticated,)
    )
    def blocked(self, request, pk=None):
        song = Song.objects.get(pk=pk)
        user = self.request.user
        serializer = BlockedSongSerializerPost(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user, song=song)
            return Response(
                f"{song.title} is in blacklist now!", status=status.HTTP_201_CREATED
            )


class BlockedSongViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = BlockedSong.objects.all()
    serializer_class = BlockedSongSerializerGet
