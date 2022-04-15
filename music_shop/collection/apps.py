from django.apps import AppConfig


class CollectionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "collection"

    def ready(self):
        from django.db.models.signals import post_save

        from collection.signals import add_collection_signal
        from user.models import CustomUser

        post_save.connect(add_collection_signal, sender=CustomUser)
