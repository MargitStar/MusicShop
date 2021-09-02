import json

import pytest
from model_bakery import baker

from song.models import Song

from ..confest import api_client, create_song, get_token

pytestmark = pytest.mark.django_db


class TestPlaylistEndpoints:

    endpoint = "/api/collections/"

    def test_list(self, api_client, get_token):
        client = api_client()
        get_token(client)

        response = client.get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_retrieve(self, api_client, get_token):
        client = api_client()
        user = get_token(client)
        collection_id = user.collection.id
        url = f"{self.endpoint}{collection_id}/"

        response = client.get(url)
        assert response.status_code == 200

    def test_unlike(self, api_client, get_token):
        song = baker.make(Song)
        client = api_client()
        user = get_token(client)
        collection = user.collection
        collection.song.add(song)
        collection_id = collection.id
        url = f"{self.endpoint}{collection_id}/unlike/{song.id}/"
        response = client.delete(url)
        assert response.status_code == 204
