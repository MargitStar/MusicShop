from rest_framework import routers
from django.urls import path

from song.views import SongDataCreateView, SongViewSet

router = routers.SimpleRouter()
router.register(r"songs", SongViewSet, basename="song")
router.register(r"data", SongDataCreateView, basename="song-data")
urlpatterns = router.urls
urlpatterns += [
    path('songs/<int:pk>/playlist/<int:playlist_id>/', SongViewSet.as_view({"get": "playlist"}))
]
