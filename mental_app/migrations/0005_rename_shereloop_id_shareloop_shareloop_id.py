# Generated by Django 4.1.7 on 2023-11-21 00:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mental_app', '0004_rename_user_id_shareloop_shereloop_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shareloop',
            old_name='shereloop_id',
            new_name='shareLoop_id',
        ),
    ]
