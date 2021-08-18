from author.models import Author
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Author
        fields = ('id', 'name', 'surname')
