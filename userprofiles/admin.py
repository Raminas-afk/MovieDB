from django.contrib import admin
from userprofiles.models import SeenMovie, SavedMovie, Profile, Comment


# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

admin.site.register(SeenMovie)
admin.site.register(Profile)
admin.site.register(SavedMovie)
admin.site.register(Comment)
