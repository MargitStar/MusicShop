from rest_framework import serializers

from collection.models import Collection
from song.serializers import SongSerializerGet


class CollectionSerializer(serializers.ModelSerializer):
    song = SongSerializerGet(many=True)

    class Meta:
        model = Collection
        fields = ("id", "user", "song")
