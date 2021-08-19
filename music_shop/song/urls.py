from rest_framework import routers

from song.views import SongViewSet, SongDataCreateView

router = routers.SimpleRouter()
router.register(r'songs', SongViewSet, basename='song')
router.register(r'data', SongDataCreateView, basename='song-data')
urlpatterns = router.urls
