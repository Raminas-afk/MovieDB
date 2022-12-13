from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('search/', views.search, name="search"),
    path('add_or_delete/', views.add_or_remove, name="add-or-remove"),
    path('movie_detail/', views.movie_detail, name="movie-detail")
]
