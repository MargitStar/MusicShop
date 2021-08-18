from django.http import FileResponse
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from song.models import Song
from song.serializers import SongSerializer


class SongViewSet(ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ('date', 'author__name', 'author__surname', 'title', 'genre__name')
    search_fields = ['^title']
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    @action(detail=True, methods=['get'])
    def data(self, request, pk=None):
        instance = Song.objects.get(pk=pk)
        file_handle = instance.data.open()

        response = FileResponse(file_handle, content_type='audio/')
        response['Content-Length'] = instance.data.size
        response['Content-Disposition'] = 'attachment; filename="%s"' % instance.data.name
        return response
