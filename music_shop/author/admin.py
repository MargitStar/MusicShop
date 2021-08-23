from author.models import Author
from django.contrib import admin


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "surname")


admin.site.register(Author, AuthorAdmin)
