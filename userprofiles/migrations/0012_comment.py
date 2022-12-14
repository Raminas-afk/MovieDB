# Generated by Django 4.1.4 on 2022-12-16 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0011_savedmovie_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=1000)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='userprofiles.seenmovie')),
                ('profile', models.ManyToManyField(related_name='profile', to='userprofiles.profile')),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
    ]
