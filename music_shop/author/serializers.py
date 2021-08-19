from rest_framework import serializers

from author.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Author
        fields = ("id", "name", "surname")
