from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from author.models import Author
from author.serializers import AuthorSerializer


class AuthorViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        queryset = Author.objects.all()
        serializer = AuthorSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = Author.objects.all()
        playlist = get_object_or_404(queryset, pk=pk)
        serializer = AuthorSerializer(playlist, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
