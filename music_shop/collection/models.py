from django.contrib.auth import get_user_model
from django.db import models

from song.models import Song

User = get_user_model()


class Collection(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="collection"
    )
    song = models.ManyToManyField(Song, blank=True, null=True)

    def __str__(self):
        return f"Collection {self.user.username}"
