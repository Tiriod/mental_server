# Generated by Django 4.1.7 on 2023-11-21 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mental_app', '0006_rename_shareloop_copy_writing_shareloop_shareloop_copy_writing'),
    ]

    operations = [
        migrations.AddField(
            model_name='meditation',
            name='meditation_type',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
