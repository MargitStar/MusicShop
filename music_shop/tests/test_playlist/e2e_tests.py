import json

import pytest
from model_bakery import baker

from playlist.models import Playlist

from ..confest import api_client, create_song, get_token

pytestmark = pytest.mark.django_db


class TestPlaylistEndpoints:

    endpoint = "/api/playlists/"

    def test_list(self, api_client):
        baker.make(Playlist, _quantity=3)

        response = api_client().get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_retrieve(self, api_client):
        playlist = baker.make(Playlist)
        url = f"{self.endpoint}{playlist.id}/"

        response = api_client().get(url)
        assert response.status_code == 200

    def test_create(self, api_client, get_token, create_song):
        playlist = baker.make(Playlist)
        song = create_song
        expected_json = {"name": playlist.name, "song": [song.id]}
        client = api_client()
        get_token(client)
        response = client.post(self.endpoint, data=expected_json, format="json")
        assert response.status_code == 201
        assert json.loads(response.content) == expected_json

    def test_update(self, api_client, get_token, create_song):
        old_playlist = baker.make(Playlist)
        new_playlist = baker.prepare(Playlist)
        song = create_song
        playlist_dict = {"name": new_playlist.name, "song": [song.id]}

        url = f"{self.endpoint}{old_playlist.id}/"

        client = api_client()
        get_token(client)

        response = client.put(url, playlist_dict, format="json")

        assert response.status_code == 200
        assert json.loads(response.content) == playlist_dict

    def test_delete(self, api_client, get_token):
        playlist = baker.make(Playlist)
        client = api_client()
        get_token(client)

        url = f"{self.endpoint}{playlist.id}/"

        response = client.delete(url)

        assert response.status_code == 204
        assert Playlist.objects.all().count() == 0
