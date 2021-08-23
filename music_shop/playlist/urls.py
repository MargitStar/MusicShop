from rest_framework import routers

from playlist.views import PlaylistViewSet

router = routers.SimpleRouter()
router.register(r"playlists", PlaylistViewSet)
urlpatterns = router.urls
