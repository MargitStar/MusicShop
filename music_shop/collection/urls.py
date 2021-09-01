from rest_framework import routers

from collection.views import CollectionViewSet

router = routers.SimpleRouter()
router.register(r"collections", CollectionViewSet, basename="collection")
urlpatterns = router.urls
