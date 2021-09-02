import json

import pytest
from model_bakery import baker

from playlist.models import Playlist

from ..confest import api_client, create_song, create_user

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

    def test_create(self, api_client, create_user, create_song):
        playlist = baker.prepare(Playlist)
        count = Playlist.objects.count()

        expected_json = {"name": playlist.name, "song": [create_song.id]}

        client = api_client()
        create_user(client)
        response = client.post(self.endpoint, data=expected_json, format="json")

        assert response.status_code == 201
        assert Playlist.objects.count() == count + 1
        assert Playlist.objects.filter(pk=response.data["id"])

    def test_update(self, api_client, create_user, create_song):
        old_playlist = baker.make(Playlist)
        new_playlist = baker.prepare(Playlist)

        playlist_dict = {
            "id": old_playlist.id,
            "name": new_playlist.name,
            "song": [create_song.id],
        }

        url = f"{self.endpoint}{old_playlist.id}/"

        client = api_client()
        create_user(client)

        response = client.put(url, playlist_dict, format="json")

        assert response.status_code == 200
        assert json.loads(response.content) == playlist_dict

    def test_delete(self, api_client, create_user):
        client = api_client()
        user = create_user(client)

        playlist = baker.make(Playlist, user=user)

        assert Playlist.objects.filter(pk=playlist.pk)

        url = f"{self.endpoint}{playlist.pk}/"

        response = client.delete(url)

        assert response.status_code == 204
        assert not Playlist.objects.filter(pk=playlist.pk)
