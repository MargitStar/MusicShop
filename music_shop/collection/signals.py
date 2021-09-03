from collection.models import Collection


def add_collection_signal(sender, instance, created, **kwargs):
    if created:
        create = Collection.objects.create(user=instance)
        create.save()
