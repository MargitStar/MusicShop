from django.db import models

from author.models import Author
from genre.models import Genre


class SongData(models.Model):
    data = models.FileField(
        upload_to='music'
    )

    def __str__(self):
        return f'Song Data {self.pk}'


class Song(models.Model):
    title = models.CharField(
        max_length=100,
    )

    author = models.ManyToManyField(
        Author,
    )

    date = models.DateField(

    )

    genre = models.ManyToManyField(
        Genre,
    )

    data = models.OneToOneField(
        SongData,
        on_delete=models.CASCADE,
        verbose_name='song'
    )

    def __str__(self):
        return self.title
