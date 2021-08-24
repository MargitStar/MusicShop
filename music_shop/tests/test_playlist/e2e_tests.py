import json

import factory
import pytest
from model_bakery import baker

from playlist.models import Playlist

pytestmark = pytest.mark.django_db


class TestPlaylistEndpoints:

    endpoint = "/api/playlist/"

    def test_list(self, api_client):
        baker.make(Playlist, _quantity=3)

        response = api_client().get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_create(self, api_client):
        playlist = baker.prepare(Playlist)
        expected_json = {
            "name": playlist.name,
            "user": playlist.user,
            "song": playlist.song,
        }

        response = api_client().post(self.endpoint, data=expected_json, format="json")

        assert response.status_code == 201
        assert json.loads(response.content) == expected_json
