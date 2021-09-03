import json

import pytest
from model_bakery import baker

from collection.models import Collection
from song.models import Song

from ..confest import api_client, create_song, create_user

pytestmark = pytest.mark.django_db


class TestPlaylistEndpoints:

    endpoint = "/api/collections/"

    def test_list(self, api_client, create_user):
        client = api_client()
        create_user(client)

        response = client.get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_retrieve_success(self, api_client, create_user):
        client = api_client()
        user = create_user(client)
        collection_id = user.collection.id
        url = f"{self.endpoint}{collection_id}/"

        response = client.get(url)
        assert response.status_code == 200

    def test_retrieve_not_found(self, api_client, create_user):
        client = api_client()
        user = create_user(client)
        collection = user.collection
        url = f"{self.endpoint}{collection.id}/"

        collection.delete()

        response = client.get(url)
        assert response.status_code == 404

    def test_unlike(self, api_client, create_user):
        song = baker.make(Song)
        client = api_client()
        user = create_user(client)
        collection = user.collection
        collection.song.add(song)
        collection_id = collection.id
        url = f"{self.endpoint}{collection_id}/unlike/{song.id}/"
        response = client.delete(url)
        assert response.status_code == 204
