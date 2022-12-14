# Generated by Django 4.1.4 on 2022-12-15 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0008_profile_saved_movies_id_profile_seen_movies_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='seenmovie',
            name='length',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='saved_movies_id',
            field=models.ManyToManyField(blank=True, to='userprofiles.savedmovie'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='seen_movies_id',
            field=models.ManyToManyField(blank=True, to='userprofiles.seenmovie'),
        ),
    ]
