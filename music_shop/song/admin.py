from django.contrib import admin

from song.models import BlockedSong, Song, SongData

admin.site.register(Song)
admin.site.register(SongData)
admin.site.register(BlockedSong)
