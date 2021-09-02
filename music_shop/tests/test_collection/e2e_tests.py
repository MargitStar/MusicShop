import json

import pytest
from django.contrib.auth.models import User
from model_bakery import baker

from collection.models import Collection

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
