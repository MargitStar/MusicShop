from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.views import SignUpViewSet

app_name = "user"
router = routers.SimpleRouter()
router.register(r"user", SignUpViewSet, basename="song")

urlpatterns = [
    *router.urls,
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
