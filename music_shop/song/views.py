from rest_framework.viewsets import ModelViewSet

from song.models import Song
from song.serializers import SongSerializer


class SongViewSet(ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
