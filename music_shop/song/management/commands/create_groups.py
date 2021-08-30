import logging

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

logging.basicConfig(level=logging.DEBUG)

GROUPS = ["Moderator", "User"]


class Command(BaseCommand):
    help = "Creates Moderator and User groups"

    def handle(self, *args, **options):
        for group in GROUPS:
            Group.objects.get_or_create(name=group)
            logging.info(f"Add group {group}")
