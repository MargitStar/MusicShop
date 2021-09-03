# Generated by Django 3.2.6 on 2021-09-03 11:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("album", "0002_remove_album_author"), ("song", "0003_song_album")]

    operations = [
        migrations.AlterField(
            model_name="song",
            name="album",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="album",
                to="album.album",
            ),
        )
    ]
