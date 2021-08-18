from django.db import models

from author.models import Author
from genre.models import Genre


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

    data = models.FileField(

    )

    def __str__(self):
        return self.title
