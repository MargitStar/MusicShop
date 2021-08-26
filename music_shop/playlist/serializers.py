from rest_framework import serializers

from playlist.models import Playlist
from song.serializers import SongSerializerGet


class PlaylistSerializer(serializers.ModelSerializer):
    song = SongSerializerGet(many=True)

    class Meta:
        model = Playlist
        fields = ("id", "name", "user", "song")


class PlaylistSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ("id", "name", "song")
