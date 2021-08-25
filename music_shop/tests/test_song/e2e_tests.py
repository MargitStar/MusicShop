import json

import pytest
from model_bakery import baker

from song.models import Song, SongData

from ..confest import api_client, create_data

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

    def test_create(self, api_client, create_data):
        song = baker.make(Song)
        song_data, genre, author = create_data
        expected_json = {
            "title": song.title,
            "author": [author.id],
            "genre": [genre.id],
            "release_date": str(song.release_date),
            "data": song_data.id,
        }

        response = api_client().post(self.endpoint, data=expected_json, format="json")

        assert response.status_code == 201

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
