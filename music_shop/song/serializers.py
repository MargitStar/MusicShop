from rest_framework import serializers

from author.serializers import AuthorSerializer
from genre.serializers import GenreSerializer
from song.models import Song, SongData

from django.db.transaction import atomic


class SongDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SongData
        fields = ("id", "data")


class SongSerializerGet(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    author = AuthorSerializer(many=True)
    data = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name="song-data",
    )

    class Meta:
        model = Song
        fields = ("id", "title", "author", "release_date", "genre", "data")


class SongSerializerPost(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = ("id", "title", "author", "genre", "release_date", "data")

    @atomic
    def create(self, validated_data):
        genres = validated_data.pop("genre", [])
        authors = validated_data.pop("author", [])

        song = Song.objects.create(**validated_data)

        for genre in genres:
            song.genre.add(genre)

        for author in authors:
            song.author.add(author)
        return song

    @atomic
    def update(self, instance, validated_data):
        authors = validated_data.get("author")
        genres = validated_data.get("genre")
        instance.title = validated_data.get("title")
        instance.release_date = validated_data.get("release_date")

        try:
            instance.author.clear()
            instance.genre.clear()

            for author in authors:
                instance.author.add(author)

            for genre in genres:
                instance.genre.add(genre)

            instance.save()
            return instance
        except TypeError:
            instance.genre.clear()
            instance.author.clear()
            instance.save()
        return instance
