from django.shortcuts import render
import requests
# Create your views here.

key = "79221ec88bc1ebd940da8a747c92a9c7"


def index(request):
    if request.method == "GET":
        return render(request, "main/index.html")
    
    if request.method == "POST":
        movie_name = request.POST['movie']
        url = "https://api.themoviedb.org/3/search/movie?api_key={}&query={}"
        poster_url = "https://image.tmdb.org/t/p/original/"
        query = requests.get(url.format(key, movie_name)).json()
        info = {
            "id": query['results'][0]['id'],
            "poster": poster_url + query['results'][0]['poster_path'],
            "title": query['results'][0]['title'],
            "rating": query['results'][0]['vote_average'],
            "overview": query['results'][0]['overview']
        }
        return render(request, "main/index.html", {
            "movie": info
        })