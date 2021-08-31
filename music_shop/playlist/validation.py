import copy

from django.db.models import ObjectDoesNotExist

from song.models import Song


def validate_songs(request):
    songs_pk = copy.deepcopy(request.data["song"])
    request.data["song"].clear()
    if songs_pk:
        for pk in songs_pk:
            try:
                Song.objects.filter(blocked=False).get(pk=pk)
                request.data["song"].append(pk)
            except ObjectDoesNotExist:
                continue
