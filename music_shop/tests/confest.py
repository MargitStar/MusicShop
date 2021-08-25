from datetime import date

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from author.models import Author
from genre.models import Genre
from song.models import Song, SongData

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient


@pytest.fixture
def get_token():
    def _get_token(client):
        User.objects.create_user(username="Star", password="star")
        token_url = "/api/token/"
        token = client.post(token_url, {"username": "Star", "password": "star"})
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token.data["access"])
        return token

    return _get_token


@pytest.fixture
def create_data():
    author = Author.objects.create(name="gleb", surname="hleb")
    genre = Genre.objects.create(name="lal", description="pal")
    song_data = SongData.objects.create(data="music/ed-sheeran_perfect.mp3")
    return song_data, genre, author


@pytest.fixture
def create_song():
    author = Author.objects.create(name="gleb", surname="hleb")
    genre = Genre.objects.create(name="lal", description="pal")
    song_data = SongData.objects.create(data="music/ed-sheeran_perfect.mp3")
    song = Song.objects.create(title="lala", release_date=date.today(), data=song_data)
    song.genre.add(genre)
    song.author.add(author)
    song.save()
    return song
