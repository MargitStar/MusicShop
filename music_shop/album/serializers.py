from rest_framework import serializers

from album.models import Album


class AlbumSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ("id", "name", "description")
