from django.contrib import admin

from song.models import Song, SongData

admin.site.register(Song)
admin.site.register(SongData)
