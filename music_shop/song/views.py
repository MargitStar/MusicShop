from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action

from song.models import Song, SongData
from song.serializers import (SongDataSerializerGet, SongSerializerGet,
                              SongSerializerPost)


class SongDataCreateView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = SongDataSerializerGet
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
        if self.request.method == "GET":
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
