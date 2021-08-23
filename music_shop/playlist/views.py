from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from playlist.models import Playlist
from playlist.serializers import PlaylistSerializer, PlaylistSerializerPost


class PlaylistViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def create(self, request, *args, **kwargs):
        serializer = PlaylistSerializerPost(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=self.request.user)
            return Response("Created")

    def get_permissions(self):
        if self.request.method == "GET" or self.request.method == "OPTIONS":
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated,)
        return super(PlaylistViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.request.method == "GET" or self.request.method == "OPTIONS":
            return PlaylistSerializer
        elif self.request.method != "DELETE":
            return PlaylistSerializerPost
