from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm, UpdateProfileForm, UpdateUserForm
from utils.reusable_variables import key, poster_url

import requests


# Create your views here.

def profile_overview(request):
    return render(request, "userprofiles/profile_overview.html", {
        "user": request.user
    })

def edit_profile(request):
    if request.method == "GET":
        profile_form = UpdateProfileForm(instance=request.user.profile)
        user_form = UpdateUserForm(instance=request.user)
        return render(request, "userprofiles/profile_edit.html", {
            "profile_form": profile_form,
            "user_form": user_form
        })
    if request.method == "POST":
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        user_form = UpdateUserForm(request.POST, instance=request.user)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

def profile_saved_movies(request):
    user = request.user
    movies_id = user.saved_movies.all()
    saved_movies_list = []

    for id in movies_id:
        url = "https://api.themoviedb.org/3/movie/{}?api_key={}"
        query = requests.get(url.format(id, key)).json()
        info = { 
            "id": query['id'],
            "title": query['title'],
            "poster": poster_url + query['poster_path'],
        }
        saved_movies_list.append(info)
    return render(request, "userprofiles/profile_saved_movies.html", {
        "movies": saved_movies_list
    })



def profile_seen_movies(request):
    user = request.user
    movies_id = user.seen_movies.all()
    poster_url = "https://image.tmdb.org/t/p/original/"
    seen_movies_list = []

    for id in movies_id:
        url = "https://api.themoviedb.org/3/movie/{}?api_key={}"
        query = requests.get(url.format(id, key)).json()
        info = { 
            "id": query['id'],
            "title": query['title'],
            "poster": poster_url + query['poster_path'],

        }
        seen_movies_list.append(info)

    return render(request, "userprofiles/profile_seen_movies.html", {
        "movies": seen_movies_list
    })


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    form = NewUserForm()
    return render(request, 'userprofiles/register.html', {
        "register_form": form
    })

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')
    form = AuthenticationForm()
    return render(request, "userprofiles/login.html", {
        "login_form": form
    })

def logout_request(request):
	logout(request)
	return redirect("homepage")