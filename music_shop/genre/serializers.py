from rest_framework import serializers

from genre.models import Genre


class GenreSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Genre
        fields = ("id", "name", "description")
