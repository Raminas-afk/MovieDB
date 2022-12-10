from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    seen = models.ManyToManyField("SeenMovie")
    saved = models.ManyToManyField("SavedMovie")


class SeenMovie(models.Model):
    movie_id = models.CharField(max_length=50)
    favorite = models.BooleanField(default=False)
    seen_by = models.ManyToManyField(settings.AUTH_USER_MODEL)


class SavedMovie(models.Model):
    movie_id = models.CharField(max_length=50)
    saved_by = models.ManyToManyField(settings.AUTH_USER_MODEL)