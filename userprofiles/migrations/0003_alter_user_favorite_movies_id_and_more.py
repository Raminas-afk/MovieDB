# Generated by Django 4.1.4 on 2022-12-10 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0002_alter_user_favorite_movies_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='favorite_movies_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='saved_movies_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='seen_movies_id',
            field=models.IntegerField(null=True),
        ),
    ]