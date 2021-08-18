from rest_framework import serializers

from author.serializers import AuthorSerializer
from genre.serializers import GenreSerializer
from song.models import Song


class SongSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    author = AuthorSerializer(many=True)

    class Meta:
        model = Song
        fields = ('title', 'author', 'date', 'genre', 'data')
