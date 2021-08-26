from django.contrib.auth import get_user_model
from django.db import models

from author.models import Author
from genre.models import Genre

User = get_user_model()


class SongData(models.Model):
    data = models.FileField(upload_to="music")

    def __str__(self):
        return f"Song Data {self.pk}"


class Song(models.Model):
    title = models.CharField(max_length=100)
    author = models.ManyToManyField(Author)
    release_date = models.DateField()
    genre = models.ManyToManyField(Genre)
    data = models.OneToOneField(SongData, on_delete=models.CASCADE, verbose_name="song")

    def __str__(self):
        return self.title


class BlockedSong(models.Model):
    song = models.OneToOneField(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)

    def __str__(self):
        return f"Blocked {self.song.title}"
