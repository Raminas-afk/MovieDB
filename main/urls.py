from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name="homepage"),
    path('add_movie/', views.add_to_list, name="add-to-list")
    # re_path(r'^add_seen/(?P<movie_id>[0-9])/$', views.add_to_seen, name='add_seen')
]
