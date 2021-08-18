from genre.models import Genre
from rest_framework import serializers


class GenreSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Genre
        fields = ('id', 'name', 'description')
