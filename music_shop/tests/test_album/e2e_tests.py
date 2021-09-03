import json

import pytest
from model_bakery import baker

from album.models import Album

from ..confest import api_client, create_song, create_user

pytestmark = pytest.mark.django_db


class TestAlbumEndpoints:

    endpoint = "/api/albums/"

    def test_list(self, api_client):
        baker.make(Album, _quantity=3)

        response = api_client().get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_retrieve_success(self, api_client):
        album = baker.make(Album)
        url = f"{self.endpoint}{album.id}/"

        response = api_client().get(url)
        assert response.status_code == 200

    def test_retrieve_not_found(self, api_client):
        album = baker.prepare(Album, id=1)
        url = f"{self.endpoint}{album.id}/"

        response = api_client().get(url)
        assert response.status_code == 404

    def test_create(self, api_client):
        album = baker.prepare(Album)
        count = Album.objects.count()

        expected_json = {"name": album.name, "description": album.description}
        client = api_client()

        response = client.post(self.endpoint, data=expected_json, format="json")

        assert response.status_code == 201
        assert Album.objects.count() == count + 1
        assert Album.objects.filter(pk=response.data["id"])

    def test_update(self, api_client, create_user, create_song):
        old_album = baker.make(Album)
        new_album = baker.prepare(Album)

        playlist_dict = {
            "id": old_album.id,
            "name": new_album.name,
            "description": new_album.description,
        }

        url = f"{self.endpoint}{old_album.id}/"

        client = api_client()

        response = client.put(url, playlist_dict, format="json")

        assert response.status_code == 200
        assert json.loads(response.content) == playlist_dict

    def test_delete(self, api_client):
        client = api_client()

        album = baker.make(Album)

        assert Album.objects.filter(pk=album.pk)

        url = f"{self.endpoint}{album.pk}/"

        response = client.delete(url)

        assert response.status_code == 204
        assert not Album.objects.filter(pk=album.pk)
