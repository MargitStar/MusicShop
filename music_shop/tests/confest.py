import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from model_bakery import baker
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
def get_moderator_token():
    def _get_moderator_token(client):
        user = User.objects.create_user(username="Star", password="star")
        group, created = Group.objects.get_or_create(name="Moderator")
        group.user_set.add(user)
        token_url = "/api/token/"
        token = client.post(token_url, {"username": "Star", "password": "star"})
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token.data["access"])
        return token

    return _get_moderator_token


@pytest.fixture
def create_data():
    author = baker.make(Author)
    genre = baker.make(Genre)
    song_data = baker.make(SongData, _create_files=True)
    return song_data, genre, author


@pytest.fixture
def create_song():
    author = baker.make(Author, surname="foo")
    genre = baker.make(Genre)
    data = baker.make(SongData, _create_files=True)
    song = baker.make(Song)
    song.genre.add(genre)
    song.author.add(author)
    song.data = data
    song.save()
    return song
