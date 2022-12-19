from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image
# Create your models here.

# class User(AbstractUser):
#     seen_movies_id = models.ManyToManyField("SeenMovie")
#     saved_movies_id = models.ManyToManyField("SavedMovie")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.CharField(max_length=300)
    seen_movies_id = models.ManyToManyField("SeenMovie", blank=True)
    saved_movies_id = models.ManyToManyField("SavedMovie", blank=True)

    def __str__(self):
        return self.user.username


    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)


        if img.height > 100 or img.width > 100:
            new_size = (100, 100)
            img.thumbnail(new_size)
            img.save(self.avatar.path)


class SeenMovie(models.Model):
    movie_id = models.IntegerField()
    favorite = models.BooleanField(default=False)
    profiles = models.ManyToManyField(Profile, related_name="seen_movies")  
    length = models.IntegerField()   

    def __str__(self):
        return str(self.movie_id)

class SavedMovie(models.Model):
    movie_id = models.IntegerField()
    profiles = models.ManyToManyField(Profile, related_name="saved_movies")
    length = models.IntegerField()   

    def __str__(self):
        return str(self.movie_id)

class Comment(models.Model):
    movie = models.ForeignKey(SeenMovie, on_delete=models.CASCADE, related_name="comments")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile_comments")
    content = models.TextField(max_length=1000)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return '{} Comment on '.format(self.profile, self.movie)