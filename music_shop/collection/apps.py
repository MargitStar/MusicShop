from django.apps import AppConfig


class CollectionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "collection"

    def ready(self):
        from django.contrib.auth.models import User
        from django.db.models.signals import post_save

        from collection.signals import add_collection_signal

        post_save.connect(add_collection_signal, sender=User)
