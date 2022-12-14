from django.apps import AppConfig


class UserprofilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userprofiles'

    def ready(self):
        import userprofiles.signals