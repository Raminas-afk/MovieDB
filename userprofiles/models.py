from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from PIL import Image
# Create your models here.

class User(AbstractUser):
    seen_movies_id = models.ManyToManyField("SeenMovie")
    saved_movies_id = models.ManyToManyField("SavedMovie")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

    def __str__(self):
        return self.user.username


class SeenMovie(models.Model):
    movie_id = models.IntegerField()
    favorite = models.BooleanField(default=False)
    seen_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="seen_movies")

    def save_model(self, request):      # ??
        SeenMovie.seen_by = request.user
        super().save_model(request)        

    def __str__(self):
        return str(self.movie_id)

class SavedMovie(models.Model):
    movie_id = models.IntegerField()
    saved_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="saved_movies")
     
    def __str__(self):
        return str(self.movie_id)
