import json

import pytest
from model_bakery import baker

from playlist.models import Playlist

from ..confest import api_client, create_test_user

pytestmark = pytest.mark.django_db


class TestPlaylistEndpoints:

    endpoint = "/api/playlists/"

    def test_list(self, api_client):
        baker.make(Playlist, _quantity=3)

        response = api_client().get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_delete(self, api_client):
        playlist = baker.make(Playlist)

        create_test_user()
        token_url = "/api/token/"
        token = api_client().post(token_url, {"username": "Star", "password": "star"})

        client = api_client()
        url = f"{self.endpoint}{playlist.id}/"
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token.data["access"])
        response = client.delete(url)

        assert response.status_code == 204
        assert Playlist.objects.all().count() == 0
