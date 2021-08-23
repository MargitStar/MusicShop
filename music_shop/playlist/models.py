from django.contrib.auth import get_user_model
from django.db import models
from song.models import Song

User = get_user_model()


class Playlist(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    song = models.ManyToManyField(Song, blank=True, null=True)

    def __str__(self):
        return self.name
