# Generated by Django 3.2.6 on 2021-08-26 10:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("genre", "0001_initial"),
        ("author", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="SongData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data", models.FileField(upload_to="music")),
            ],
        ),
        migrations.CreateModel(
            name="Song",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("release_date", models.DateField()),
                ("author", models.ManyToManyField(to="author.Author")),
                (
                    "data",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="song.songdata",
                        verbose_name="song",
                    ),
                ),
                ("genre", models.ManyToManyField(to="genre.Genre")),
            ],
        ),
        migrations.CreateModel(
            name="BlockedSong",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("comment", models.TextField(max_length=500)),
                (
                    "song",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="song.song"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
