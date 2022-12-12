from django.shortcuts import render, redirect
from userprofiles.models import SeenMovie, SavedMovie
from utils.reusable_functions import is_movie_saved, is_movie_seen
from utils.reusable_variables import key, poster_url, trailer_url
import requests

# Reusable variables


# A few functions


# Create your views here.

def homepage(request):
    if request.method == "GET":
        return render(request, "main/homepage.html")
    

    if request.method == "POST":
        movie_name = request.POST['movie']
        url = "https://api.themoviedb.org/3/search/movie?api_key={}&query={}"
        query = requests.get(url.format(key, movie_name)).json()
        results = query['results']

        search_results = []
        result_nr = 0
        for item in results:
            try:
                info = {
                    "id": results[result_nr]['id'],
                    "poster": poster_url + results[result_nr]['poster_path'],
                    "title": results[result_nr]['title'],
                    "rating": results[result_nr]['vote_average'],
                    "overview": results[result_nr]['overview']
                }
                search_results.append(info)
                result_nr += 1
            except:
                pass
        return render(request, "main/homepage.html", {
            "search_results": search_results,
        })


def movie_detail(request):
    current_user = request.user
    if request.method == "POST":
        movie_id = request.POST['movie_id']
        url = "https://api.themoviedb.org/3/movie/{}?api_key={}"
        query = requests.get(url.format(movie_id, key)).json()
        trailer_query = requests.get(trailer_url.format(movie_id, key)).json()
        info = {
            "id": query['id'],
            "poster": poster_url + query['poster_path'],
            "trailer_key": trailer_query['results'][0]['key'],
            "title": query['title'],
            "rating": query['vote_average'],
            "overview": query['overview'],    #Additional parameter genre_name[integer], some logic below
        }
        genres_list = query['genres']
        genre_nr = 1
        for item in genres_list:
            info[f"genre_name_{genre_nr}"] = item['name']
            genre_nr += 1

        print(info)   # for easier debugging

        return render(request, "main/movie_detail.html", {
            "movie": info,
            "movie_id": movie_id,  # delete if not needed
            "exists_in_seen": is_movie_seen(movie_id, current_user),
            "exists_in_later": is_movie_saved(movie_id, current_user)
        })

def add_or_remove(request):
    current_user = request.user
    if request.method == "POST":
        if "seen_movie" in request.POST:
            movie_id = request.POST['seen_movie']
            try:
                existing_movie = SeenMovie.objects.get(movie_id=movie_id)  #check if instance exists in database(that means some user created it)
                try:
                    existing_movie = SeenMovie.objects.get(movie_id=movie_id, seen_by=current_user) #check if instance is associated with current user
                except:
                    existing_movie.seen_by.add(current_user) # if it's not, add user
                    existing_movie.save()
                else:
                    existing_movie.seen_by.remove(current_user) # if it is, remove user 
                    existing_movie.save()

            except:
                new_movie = SeenMovie(movie_id=movie_id) # if instance doesnt exist, create and assign current user
                new_movie.save()
                new_movie.seen_by.add(request.user)
                new_movie.save()
            
        elif "saved_movie" in request.POST: # same logic
            movie_id = request.POST['saved_movie']
            try:
                existing_movie = SavedMovie.objects.get(movie_id=movie_id)  
                try:
                    existing_movie = SavedMovie.objects.get(movie_id=movie_id, seen_by=current_user) 
                except:
                    existing_movie.saved_by.add(current_user)
                    existing_movie.save()
                else:
                    existing_movie.saved_by.remove(current_user)
                    existing_movie.save()

            except:
                new_movie = SavedMovie(movie_id=movie_id)
                new_movie.save()
                new_movie.saved_by.add(current_user)
                new_movie.save()
        
        return redirect('homepage')