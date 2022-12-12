from django.urls import path
from . import views


urlpatterns = [
    path('profile', views.profile_overview, name="profile"),
    path('profile/seen-movies', views.profile_seen_movies, name="seen-movies"),
    path('profile/saved-movies', views.profile_saved_movies, name="saved-movies"),
    path('register', views.register_request, name="register"),
    path('login', views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
]
 