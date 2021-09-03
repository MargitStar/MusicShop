import json

import pytest
from model_bakery import baker

from collection.models import Collection
from song.models import BlockedSong, Song, SongData

from ..confest import (
    api_client,
    create_data,
    create_song,
    create_user,
    get_moderator_token,
)

pytestmark = pytest.mark.django_db


class TestSongDataEndpoints:
    endpoint = "/api/data/"

    def test_create(self, api_client):
        song_data = baker.make(SongData, _create_files=True)
        response = api_client().post(self.endpoint, data={"data": song_data.data})
        assert response.status_code == 201


class TestSongEndpoints:
    endpoint = "/api/songs/"

    def test_list(self, api_client):
        baker.make(Song, _quantity=3)

        response = api_client().get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_filter_author_name(self, api_client, create_song):
        song = create_song
        author_name = song.author.all()[0].name
        url = f"{self.endpoint}?author_name={author_name}"

        response = api_client().get(url)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_filter_author_surname(self, api_client, create_song):
        song = create_song
        author_surname = song.author.all()[0].surname
        url = f"{self.endpoint}?author_surname={author_surname}"

        response = api_client().get(url)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_filter_title(self, api_client, create_song):
        song = create_song
        title = song.title
        url = f"{self.endpoint}?title={title}"

        response = api_client().get(url)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_filter_genre(self, api_client, create_song):
        song = create_song
        genre_name = song.genre.all()[0].name
        url = f"{self.endpoint}?genre={genre_name}"

        response = api_client().get(url)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_filter_release_date(self, api_client, create_song):
        song = create_song
        release_date = song.release_date
        url = f"{self.endpoint}?release_date={release_date}"

        response = api_client().get(url)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_create(self, api_client, create_data):
        song = baker.prepare(Song)
        song_data, genre, author = create_data
        count = Song.objects.count()
        expected_json = {
            "title": song.title,
            "author": [author.id],
            "genre": [genre.id],
            "release_date": str(song.release_date),
            "data": song_data.id,
        }

        response = api_client().post(self.endpoint, data=expected_json, format="json")

        assert response.status_code == 201
        assert Song.objects.count() == count + 1
        assert Song.objects.filter(pk=response.data["id"])

    def test_retrieve(self, api_client):
        song = baker.make(Song)
        url = f"{self.endpoint}{song.id}/"

        response = api_client().get(url)
        assert response.status_code == 200

    def test_update(self, api_client, create_data):
        old_song = baker.make(Song)
        new_song = baker.prepare(Song)
        song_data, genre, author = create_data
        song_dict = {
            "id": old_song.id,
            "title": new_song.title,
            "author": [author.id],
            "genre": [genre.id],
            "release_date": str(new_song.release_date),
            "data": song_data.id,
        }

        url = f"{self.endpoint}{old_song.id}/"

        response = api_client().put(url, song_dict, format="json")
        assert response.status_code == 200
        assert json.loads(response.content) == song_dict

    def test_delete(self, api_client):
        song = baker.make(Song)
        url = f"{self.endpoint}{song.pk}/"

        response = api_client().delete(url)

        assert response.status_code == 204
        assert not Song.objects.filter(pk=song.pk)

    def test_blocked_201(self, api_client, get_moderator_token):
        song = baker.make(Song)
        blocked_song = baker.prepare(BlockedSong)
        blocked_song.song = song

        url = f"{self.endpoint}{song.pk}/blocked/"

        client = api_client()
        get_moderator_token(client)

        data = {"comment": blocked_song.comment}

        response = client.put(url, data, format="json")

        assert response.status_code == 201

    def test_blocked_200(self, api_client, get_moderator_token):
        song = baker.make(Song)
        baker.make(BlockedSong, song=song)
        new_blocked_song = baker.prepare(BlockedSong)

        url = f"{self.endpoint}{song.pk}/blocked/"
        client = api_client()
        get_moderator_token(client)

        data = {"comment": new_blocked_song.comment}

        response = client.put(url, data=data, format="json")

        assert response.status_code == 200

    def test_like_success(self, api_client, create_user):
        client = api_client()
        create_user(client)

        song = baker.make(Song)

        url = f"{self.endpoint}{song.pk}/like/"

        response = client.get(url)

        assert response.status_code == 200

    def test_like_server_error(self, api_client, create_user):
        client = api_client()
        user = create_user(client)

        song = baker.make(Song)
        collection = Collection.objects.filter(user=user)
        collection.delete()

        url = f"{self.endpoint}{song.pk}/like/"

        response = client.get(url)

        assert response.status_code == 500


class TestBlockedSongEndpoints:
    endpoint = "/api/blocked-songs/"

    def test_list(self, api_client, get_moderator_token):
        baker.make(BlockedSong, _quantity=3)

        client = api_client()
        get_moderator_token(client)

        response = client.get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_retrieve(self, api_client, get_moderator_token):
        blocked_song = baker.make(BlockedSong)
        url = f"{self.endpoint}{blocked_song.id}/"

        client = api_client()
        get_moderator_token(client)

        response = client.get(url)
        assert response.status_code == 200
