from rest_framework import routers

from song.views import SongViewSet

router = routers.SimpleRouter()
router.register(r'songs', SongViewSet)
urlpatterns = router.urls
