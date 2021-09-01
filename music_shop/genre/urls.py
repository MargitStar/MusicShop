from rest_framework import routers

from genre.views import GenreViewSet

router = routers.SimpleRouter()
router.register(r"genres", GenreViewSet, basename="genre")
urlpatterns = router.urls
