from statistics import mean
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.template import loader
from .forms import NewUserForm

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

from django.contrib import messages

from .models import Movie, Genre, Rating, Comment


# Create your views here.


def index(request : HttpRequest):
    movies = Movie.objects.order_by('-title')
    return render(request=request, template_name="userview/index.html", context={'movies': movies})


def search(request):
    return render(request=request, template_name="userview/search.html", context={})


def admin(request):
    if not request.user.is_superuser:
        return redirect('/')
    
    return render(request=request, template_name="userview/admin.html", context={})


def movie(request, *args, **kwargs):
    pk = kwargs['pk']
    movie = Movie.objects.get(pk=pk)
    comments = Comment.objects.filter(movie_id = movie.id)
    ratings = Rating.objects.filter(movie_id = movie.id)
    if ratings.count() == 0:
        avg_rating = '---'
    else:
        avg_rating = round(mean([ r.value for r in ratings]), 2)

    return render(request=request, template_name="userview/movie.html", context={'movie':movie, 'avg_rating': avg_rating, 'comments': comments})


def register_request(request):

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")

    form = NewUserForm()
    return render(request=request, template_name="userview/register.html",context={"register_form":form})


def login_request(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        
        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Login fail.")
            
        else:
            messages.error(request, "Login fail. Invalid form")

    form = AuthenticationForm()
    return render(request=request, template_name="userview/login.html", context={"login_form":form})


def logout_request(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    
    return redirect('/login')
