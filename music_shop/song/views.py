from django.http import FileResponse
from rest_framework.response import Response
from rest_framework import filters, viewsets, parsers, mixins
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from song.models import Song, SongData
from song.serializers import SongSerializerGet, SongDataSerializerGet


class SongDataCreateView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = SongDataSerializerGet
    queryset = SongData.objects.all()


class SongViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ('date', 'author__name', 'author__surname', 'title', 'genre__name')
    search_fields = ['^title']
    queryset = Song.objects.all()
    serializer_class = SongSerializerGet

    @action(detail=True, methods=['get'])
    def data(self, request, pk=None):
        instance = SongData.objects.get(pk=pk)
        file_handle = instance.data.open()

        response = FileResponse(file_handle, content_type='audio/mpeg')
        response['Content-Length'] = instance.data.size
        response['Content-Disposition'] = 'attachment; filename="%s"' % instance.data.name
        return response
