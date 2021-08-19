from rest_framework import serializers

from author.models import Author
from author.serializers import AuthorSerializer
from genre.models import Genre
from genre.serializers import GenreSerializer
from song.models import Song, SongData


class SongDataSerializerGet(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SongData
        fields = ("data",)


class SongDataSerializerPost(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = SongData
        fields = ("id",)


class SongSerializerGet(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    author = AuthorSerializer(many=True)
    data = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name="song-data",
    )

    class Meta:
        model = Song
        fields = ("title", "author", "date", "genre", "data")


class SongSerializerPost(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    author = AuthorSerializer(many=True)
    data = SongDataSerializerPost()

    class Meta:
        model = Song
        fields = ("title", "author", "genre", "date", "data")

    def create(self, validated_data):
        genre = validated_data.pop("genre", [])
        author = validated_data.pop("author", [])

        data = validated_data.pop("data")
        data_ = SongData.objects.get(pk=data.get("id"))
        song = Song.objects.create(data=data_, **validated_data)

        for current in genre:
            genre_ = Genre.objects.get(pk=current.get("id"))
            song.genre.add(genre_)

        for current in author:
            author_ = Author.objects.get(pk=current.get("id"))
            song.author.add(author_)
        return song

    @staticmethod
    def unpack_dict(dictionary):
        for key, value in dictionary.items():
            return value

    def update(self, instance, validated_data):
        author = validated_data.get("author")
        genre = validated_data.get("genre")
        instance.title = validated_data.get("title")
        instance.date = validated_data.get("date")

        try:
            for inst in author:
                instance.author.clear()
                instance.author.add(self.unpack_dict(inst))

            for inst in genre:
                instance.genre.clear()
                instance.genre.add(self.unpack_dict(inst))
            instance.save()
            return instance
        except TypeError:
            instance.genre.clear()
            instance.author.clear()
            instance.save()
        return instance
