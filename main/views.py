from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from userprofiles.models import SeenMovie
import requests

User = get_user_model()
key = "79221ec88bc1ebd940da8a747c92a9c7"


# Create your views here.

def index(request):
    if request.method == "GET":
        return render(request, "main/index.html")
    
    if request.method == "POST":
        movie_name = request.POST['movie']
        url = "https://api.themoviedb.org/3/search/movie?api_key={}&query={}"
        poster_url = "https://image.tmdb.org/t/p/original/"
        query = requests.get(url.format(key, movie_name)).json()
        id = query['results'][0]['id']
        info = {
            "id": query['results'][0]['id'],
            "poster": poster_url + query['results'][0]['poster_path'],
            "title": query['results'][0]['title'],
            "rating": query['results'][0]['vote_average'],
            "overview": query['results'][0]['overview']
        }
        return render(request, "main/index.html", {
            "movie": info,
            "movie_id": id
        })

def add_to_seen(request):
    if request.method == "POST":
            movie_id = request.POST['id']
            new_movie = SeenMovie(movie_id=movie_id)
            # new_movie.save(commit=False)
            new_movie.save()
            new_movie.seen_by.add(request.user)
            new_movie.save()
            return redirect('homepage')