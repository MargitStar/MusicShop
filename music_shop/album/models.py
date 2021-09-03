from django.db import models

from author.models import Author


class Album(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)
    author = models.ManyToManyField(Author)

    def __str__(self):
        return f"Album {self.name}"
