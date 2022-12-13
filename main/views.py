from django.shortcuts import render, redirect
from userprofiles.models import SeenMovie, SavedMovie
from utils.reusable_functions import is_movie_saved, is_movie_seen
from utils.reusable_variables import key, poster_url, trailer_url, upcoming_url, similar_url
import requests

# Reusable variables


# A few functions


# Create your views here.

def homepage(request):
    if request.method == "GET":
        query = requests.get(upcoming_url.format(key)).json()
        results = query['results']
        top3_results = []
        result_nr = 0
        for item in results:
            if result_nr < 3:
                try:
                    info = {
                        "id": results[result_nr]['id'],
                        "poster": poster_url + results[result_nr]['poster_path'],
                        "title": results[result_nr]['title'],
                        "rating": results[result_nr]['vote_average'],
                    }
                    top3_results.append(info)
                    result_nr += 1
                except:
                    pass
        return render(request, 'main/homepage.html', {
            'top3_results': top3_results
        })

def search(request):
    if request.method == "GET":
        return redirect('homepage')

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
        return render(request, "main/search.html", {
            "search_results": search_results,
        })


def movie_detail(request):
    current_user = request.user
    if request.method == "POST":
        movie_id = request.POST['movie_id']
        url = "https://api.themoviedb.org/3/movie/{}?api_key={}"
        query = requests.get(url.format(movie_id, key)).json()
        similar_query = requests.get(similar_url.format(movie_id, key)).json()
        trailer_query = requests.get(trailer_url.format(movie_id, key)).json()
        movie_detail = {
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
            movie_detail[f"genre_name_{genre_nr}"] = item['name']
            genre_nr += 1

        print(movie_detail)   # for easier debugging

        similar_movies = similar_query['results']
        similar_results = []
        similar_nr = 0
        for movie in similar_movies:
            if similar_nr < 3:
                try:
                    info = {
                        "id": similar_movies[similar_nr]['id'],
                        "poster": poster_url + similar_movies[similar_nr]['poster_path'],
                        "title": similar_movies[similar_nr]['title'],
                        "rating": similar_movies[similar_nr]['vote_average'],
                    }
                    similar_results.append(info)
                    similar_nr += 1
                except:
                    pass
        return render(request, "main/movie_detail.html", {
            "movie": movie_detail,
            "similar_movies": similar_results,
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