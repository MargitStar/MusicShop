# Generated by Django 3.2.6 on 2021-08-20 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='date',
            new_name='release_date',
        ),
    ]
