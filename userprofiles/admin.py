from django.contrib import admin

# Register your models here.

from django.contrib.auth import get_user_model
from userprofiles.models import SeenMovie, SavedMovie, Profile
# Register your models here.

User = get_user_model()

admin.site.register(User)
admin.site.register(SeenMovie)
admin.site.register(Profile)
admin.site.register(SavedMovie)
