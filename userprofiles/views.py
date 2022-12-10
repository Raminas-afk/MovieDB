from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .models import SeenMovie

User = get_user_model()


# Create your views here.

def profile_overview(request):
    movies = SeenMovie.objects.filter(seen_by=request.user)

    return render(request, "userprofiles/profile_overview.html", {
        "movies": movies
    })


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful !")
            return redirect('homepage')
        messages.error(request, "Unsuccessful registration. Check details.")
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