from django.urls import path
from rest_framework import routers

from song.views import BlockedSongViewSet, SongDataCreateView, SongViewSet

router = routers.SimpleRouter()
router.register(r"songs", SongViewSet, basename="song")
router.register(r"data", SongDataCreateView, basename="song-data")
router.register(r"blocked-songs", BlockedSongViewSet, basename="blocked-song")
urlpatterns = [
    *router.urls,
    path(
        "songs/<int:pk>/playlist/<int:playlist_id>/",
        SongViewSet.as_view({"get": "playlist"}),
    ),
]
