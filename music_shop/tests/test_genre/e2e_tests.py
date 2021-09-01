import json

import pytest
from model_bakery import baker

from genre.models import Genre

from ..confest import api_client

pytestmark = pytest.mark.django_db


class TestPlaylistEndpoints:

    endpoint = "/api/genres/"

    def test_list(self, api_client):
        baker.make(Genre, _quantity=3)

        response = api_client().get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_retrieve(self, api_client):
        playlist = baker.make(Genre)
        url = f"{self.endpoint}{playlist.id}/"

        expected_json = {
            "id": playlist.id,
            "name": playlist.name,
            "description": playlist.description,
        }

        response = api_client().get(url)
        assert response.status_code == 200
        assert json.loads(response.content) == expected_json
