from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"
