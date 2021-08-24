import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from author.models import Author
from genre.models import Genre
from song.models import SongData

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient


@pytest.mark.django_db
def create_test_user():
    user = User.objects.create_user(username="Star", password="star")
    return user


@pytest.mark.django_db
def create_data():
    author = Author.objects.create(name="gleb", surname="hleb")
    genre = Genre.objects.create(name="lal", description="pal")
    song_data = SongData.objects.create(data="music/ed-sheeran_perfect.mp3")
    return song_data, genre, author
