# Generated by Django 4.1.4 on 2022-12-14 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0005_alter_savedmovie_saved_by_alter_seenmovie_seen_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(max_length=300),
        ),
    ]
