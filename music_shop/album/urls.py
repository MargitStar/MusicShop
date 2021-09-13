from rest_framework import routers

from album.views import AlbumViewSet

router = routers.SimpleRouter()
router.register(r"albums", AlbumViewSet, basename="albums")
urlpatterns = router.urls
