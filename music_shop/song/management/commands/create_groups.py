from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

GROUPS = ["Moderator", "User"]


class Command(BaseCommand):
    help = "Creates Moderator and User groups"

    def handle(self, *args, **options):
        for group in GROUPS:
            Group.objects.get_or_create(name=group)
