from rest_framework import serializers

from author.models import Author
from author.serializers import AuthorSerializer
from genre.models import Genre
from genre.serializers import GenreSerializer
from song.models import Song


class SongSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    author = AuthorSerializer(many=True)

    class Meta:
        model = Song
        fields = ('title', 'author', 'date', 'genre', 'data')

    def create(self, validated_data):
        genre = validated_data.pop('genre', [])
        author = validated_data.pop('author', [])
        song = Song.objects.create(**validated_data)

        for current in genre:
            genre_ = Genre.objects.get(pk=current.get('id'))
            song.genre.add(genre_)

        for current in author:
            author_ = Author.objects.get(pk=current.get('id'))
            song.author.add(author_)
        return song

    @staticmethod
    def unpack_dict(dictionary):
        for key, value in dictionary.items():
            return value

    def update(self, instance, validated_data):
        author = validated_data.get('author')
        genre = validated_data.get('author')
        instance.title = validated_data.get('title')
        instance.data = validated_data.get('data')
        instance.date = validated_data.get('date')

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
