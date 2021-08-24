import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient


@pytest.mark.django_db
def create_test_user():
    user = User.objects.create_user(username="Star", password="star")
    return user
