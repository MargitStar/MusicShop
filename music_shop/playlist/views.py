from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response


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
        if self.request.method != "GET":
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (AllowAny,)
        return super(PlaylistViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PlaylistSerializer
        elif self.request.method != "DELETE":
            return PlaylistSerializerPost
