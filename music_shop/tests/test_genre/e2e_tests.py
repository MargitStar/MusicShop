import json

import pytest
from model_bakery import baker

from genre.models import Genre

from ..confest import api_client

pytestmark = pytest.mark.django_db


class TestGenreEndpoints:

    endpoint = "/api/genres/"

    def test_list(self, api_client):
        baker.make(Genre, _quantity=3)

        response = api_client().get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_retrieve_200(self, api_client):
        genre = baker.make(Genre)
        url = f"{self.endpoint}{genre.id}/"

        expected_json = {
            "id": genre.id,
            "name": genre.name,
            "description": genre.description,
        }

        response = api_client().get(url)
        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_retrieve_404(self, api_client):
        genre = baker.prepare(Genre, id=1)
        url = f"{self.endpoint}{genre.id}/"

        response = api_client().get(url)
        assert response.status_code == 404
