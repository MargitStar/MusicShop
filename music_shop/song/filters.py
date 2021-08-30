import django_filters

from song.models import Song


class SongFilter(django_filters.FilterSet):
    release_date = django_filters.DateFilter(field_name="release_date")
    author_name = django_filters.CharFilter(field_name="author__name")
    author_surname = django_filters.CharFilter(field_name="author__surname")
    title = django_filters.CharFilter(field_name="title")
    genre = django_filters.CharFilter(field_name="genre__name")

    class Meta:
        model = Song
        fields = ["release_date", "author_name", "author_surname", "title", "genre"]
