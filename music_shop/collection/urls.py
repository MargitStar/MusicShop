from django.urls import path
from rest_framework import routers

from collection.views import CollectionViewSet

router = routers.SimpleRouter()
router.register(r"collections", CollectionViewSet, basename="collection")
urlpatterns = [
    *router.urls,
    path(
        "collections/<int:pk>/unlike/<int:song_id>/",
        CollectionViewSet.as_view({"delete": "unlike"}),
    ),
]
