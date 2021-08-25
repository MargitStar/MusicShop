import json

import pytest
from model_bakery import baker

from playlist.models import Playlist

from ..confest import api_client, get_token

pytestmark = pytest.mark.django_db


class TestPlaylistEndpoints:

    endpoint = "/api/playlists/"

    def test_list(self, api_client):
        baker.make(Playlist, _quantity=3)

        response = api_client().get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_delete(self, api_client, get_token):
        playlist = baker.make(Playlist)
        client = api_client()
        get_token(client)

        url = f"{self.endpoint}{playlist.id}/"

        response = client.delete(url)

        assert response.status_code == 204
        assert Playlist.objects.all().count() == 0
