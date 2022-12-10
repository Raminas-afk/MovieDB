from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name="homepage"),
    path('add_seen/', views.add_to_seen, name="add_seen")
    # re_path(r'^add_seen/(?P<movie_id>[0-9])/$', views.add_to_seen, name='add_seen')
]
