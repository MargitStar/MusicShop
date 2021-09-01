import json

import pytest
from model_bakery import baker

from author.models import Author

from ..confest import api_client

pytestmark = pytest.mark.django_db


class TestAuthorEndpoints:

    endpoint = "/api/authors/"

    def test_list(self, api_client):
        baker.make(Author, _quantity=3)

        response = api_client().get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_retrieve(self, api_client):
        author = baker.make(Author)
        url = f"{self.endpoint}{author.id}/"

        expected_json = {
            "id": author.id,
            "name": author.name,
            "surname": author.surname,
        }

        response = api_client().get(url)
        assert response.status_code == 200
        assert json.loads(response.content) == expected_json
