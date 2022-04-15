from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from genre.models import Genre
from genre.serializers import GenreSerializer


class GenreViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        queryset = Genre.objects.all()
        serializer = GenreSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        genre = get_object_or_404(Genre, pk=pk)
        serializer = GenreSerializer(genre, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True, methods=["get"], permission_classes=(permissions.IsAuthenticated,)
    )
    def like(self, request, pk=None):
        genre = get_object_or_404(Genre, pk=pk)
        user = self.request.user
        user.favourite_genre.add(genre)
        user.save()
        return Response(
            f"{genre.name} is added to your favourite genres!",
            status=status.HTTP_200_OK,
        )
