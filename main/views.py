from django.shortcuts import render, redirect
from userprofiles.models import SeenMovie, SavedMovie, Profile, Comment
from .forms import CommentForm
from utils.reusable_functions import is_movie_saved, is_movie_seen
from utils.reusable_variables import key, poster_url, trailer_url, upcoming_url, similar_url, top_rated_url, popular_url
import requests


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

def movies_section(request, section):
    if request.method == "GET":
        url = ""
        if section == "top_rated":
            url = top_rated_url
        elif section == "upcoming":
            url = upcoming_url
        elif section == "popular":
            url = popular_url
        query = requests.get(url.format(key)).json()
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


def movie_detail(request, movie_id):
    current_profile = Profile.objects.get(user=request.user)

    if request.method == "GET":
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
            "length": query['runtime'],
            "overview": query['overview'],    #Additional parameter  genre_name[integer] added from below
        }
        genres_list = query['genres']
        genre_nr = 1
        for item in genres_list:
            movie_detail[f"genre_name_{genre_nr}"] = item['name']
            genre_nr += 1

        print(movie_detail)   # for terminal view

        similar_movies = similar_query['results']
        similar_results = []
        similar_nr = 0
        for movie in similar_movies: # try in range()
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
        # try:
        #     movie = SeenMovie.objects.get(movie_id=movie_id)          # Fix Comment section
        #     comments = movie.comments.filter(active=True)
        # except:
        #     pass

        # comments = movie.comments.filter(active=True)
        # comments = Comment.objects.filter(movie=movie_id)
        # new_comment = None
        # comment_form = CommentForm()
        
    # if request.method == "POST":      
    #     comment_form = CommentForm(data=request.POST)
    #     if comment_form.is_valid():
    #         movie_length = request.POST['movie_length']
    #         movie = SeenMovie.objects.get_or_create(movie_id=movie_id, length=movie_length)
    #         new_comment = comment_form.save(commit=False)
    #         new_comment.movie = movie
    #         new_comment.profile = current_profile
    #         new_comment.save()
        
            # return redirect('movie-detail', movie_id=movie_id)
            
    return render(request, "main/movie_detail.html", {
        "movie": movie_detail,
        "similar_movies": similar_results,
        "exists_in_seen": is_movie_seen(movie_id, current_profile),
        "exists_in_later": is_movie_saved(movie_id, current_profile),
        # "comments": comments,
        # "new_comment": new_comment,   # Comment section
        # "comment_form": comment_form
    })

def add_or_remove(request):
    if request.method == "POST":
        if "seen_movie" in request.POST:
            model = SeenMovie
            movie_id = request.POST['seen_movie']
        else:
            model = SavedMovie
            movie_id = request.POST['saved_movie']
        
        movie_length = request.POST['movie_length']

        try:
            existing_movie = model.objects.get(movie_id=movie_id)  #check if instance exists in database(that means some profile created it)
            try:
                existing_movie = model.objects.get(movie_id=movie_id, profiles=request.user.profile) #check if instance is associated with current profile
            except:
                existing_movie.profiles.add(request.user.profile) # if it's not, add profile
                existing_movie.save()
            else:
                existing_movie.profiles.remove(request.user.profile) # if it is, remove profile
                existing_movie.save()

        except:
            new_movie = model(movie_id=movie_id, length=movie_length) # if instance doesnt exist, create and assign current profile
            new_movie.save()
            new_movie.profiles.add(request.user.profile)
            new_movie.save()
            
        return redirect('movie-detail', movie_id = movie_id)