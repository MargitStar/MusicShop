from rest_framework import serializers

from author.serializers import AuthorSerializer
from genre.serializers import GenreSerializer
from song.models import BlockedSong, Song, SongData


class SongDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SongData
        fields = ("id", "data")


class SongSerializerGet(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    author = AuthorSerializer(many=True)
    data = serializers.HyperlinkedRelatedField(read_only=True, view_name="song-data")

    class Meta:
        model = Song
        fields = ("id", "title", "author", "release_date", "genre", "data")


class SongSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ("id", "title", "author", "genre", "release_date", "data")


class BlockedSongSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = BlockedSong
        fields = ("comment",)


class BlockedSongSerializerGet(serializers.ModelSerializer):
    song = SongSerializerGet()

    class Meta:
        model = BlockedSong
        fields = ("id", "song", "user", "comment")
