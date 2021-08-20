from rest_framework import serializers

from genre.models import Genre


class GenreSerializerGet(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Genre
        fields = ("id", "name", "description")


class GenreSerializerPost(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Genre
        fields = ("id",)
