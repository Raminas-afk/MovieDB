from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    seen_movies_id = models.ManyToManyField("SeenMovie")
    saved_movies_id = models.ManyToManyField("SavedMovie")


class SeenMovie(models.Model):
    movie_id = models.IntegerField()
    favorite = models.BooleanField(default=False)
    seen_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="seen_movies")

    def save_model(self, request):
        SeenMovie.seen_by = request.user
        super().save_model(request)

    def __str__(self):
        return str(self.movie_id)

class SavedMovie(models.Model):
    movie_id = models.IntegerField()
    saved_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="saved_movies")
     
    def __str__(self):
        return str(self.movie_id)
