from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from author.models import Author
from author.serializers import AuthorSerializer


class AuthorViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        queryset = Author.objects.all()
        serializer = AuthorSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        author = get_object_or_404(Author, pk=pk)
        serializer = AuthorSerializer(author, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True, methods=["get"], permission_classes=(permissions.IsAuthenticated,)
    )
    def like(self, request, pk=None):
        author = get_object_or_404(Author, pk=pk)
        user = self.request.user
        user.favourite_author.add(author)
        user.save()
        return Response(
            f"{author.name} is added to your favourite authors!",
            status=status.HTTP_200_OK,
        )
