# Generated by Django 4.1.7 on 2023-11-20 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mental_app', '0002_remove_audio_audio_data_audio_audio_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shareloop',
            name='image_list_id',
        ),
        migrations.AddField(
            model_name='shareloop',
            name='image_id_list',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]