import json

import factory
import pytest
from model_bakery import baker

from song.models import Song

from ..confest import api_client

pytestmark = pytest.mark.django_db


class TestSongEndpoints:

    endpoint = "/api/songs/"

    def test_list(self, api_client):
        baker.make(Song, _quantity=3)

        response = api_client().get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_delete(self, api_client):
        song = baker.make(Song)
        url = f"{self.endpoint}{song.id}/"

        response = api_client().delete(url)

        assert response.status_code == 204
        assert Song.objects.all().count() == 0
