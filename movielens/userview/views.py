from statistics import mean
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.template import loader
from .forms import NewUserForm, NewMovieForm, RateMovieForm, NewCommentForm, SearchForm

from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm

from django.contrib import messages

from .models import Movie, Genre, Rating, Comment



# Create your views here.


def index(request : HttpRequest):
    movies = Movie.objects.order_by('-title')[0:10]
    data = []
    for movie in movies:
        ratings = Rating.objects.filter(movie_id = movie.id)
        if ratings.count() == 0:
            avg_rating = '---'
        else:
            avg_rating = round(mean([ r.value for r in ratings]), 2)
        data.append([movie, avg_rating])


    return render(request=request, template_name="userview/index.html", context={'movies': data})


def search(request : HttpRequest):
    search_form = SearchForm()
    context = {'search_form':search_form}

    if request.method == "POST":
        form = SearchForm(request.POST)

        if not form.is_valid():
            return render(request=request, template_name="userview/search.html", context=context)
        
        movie_title = form.cleaned_data.get('movie')
        genre = form.cleaned_data.get('genre')
        minimal_rating = form.cleaned_data.get('rating')

        results = None

        if movie_title:
            res = []
            movies = Movie.objects.filter(title__icontains=movie_title)
            for movie in movies:
                ratings = Rating.objects.filter(movie_id = movie.id)
                avg_rating = "---"
                if ratings.count() != 0:    
                    avg_rating = round(mean([ r.value for r in ratings]), 2)
                res.append([movie, avg_rating])
            
            if len(res) > 0:
                results = res                      
        
        elif genre:
            res = []
            for movie in Movie.objects.all():
                if movie.genres.filter(name__icontains=genre).count() > 0: 
                    ratings = Rating.objects.filter(movie_id = movie.id)
                    avg_rating = "---"
                    if not ratings.count() == 0:    
                        avg_rating = round(mean([ r.value for r in ratings]), 2)
                    res.append([movie, avg_rating])
            
            if len(res) > 0:
                results = res
        
        elif minimal_rating and int(minimal_rating) != 0:
            res = []
            for movie in Movie.objects.all():
                ratings = Rating.objects.filter(movie_id = movie.id)
                if ratings.count() == 0:
                    continue
                
                avg_rating = round(mean([ r.value for r in ratings]), 2)
                if avg_rating >= int(minimal_rating):
                    res.append([movie, avg_rating])            
            
            if len(res) > 0:
                results = res

        if results:
            context['results'] = results
        else:
            context['no_results'] = True

    return render(request=request, template_name="userview/search.html", context=context)


def admin(request : HttpRequest):
    if not request.user.is_superuser:
        return redirect('/')
    
    if request.method == "POST":
        movie_form = NewMovieForm(request.POST)

        if movie_form.is_valid():
            title = movie_form.cleaned_data.get('title')
            genres = movie_form.cleaned_data.get('genres_field')
            imdb = movie_form.cleaned_data.get('IMDB')

            movie = Movie.objects.create()
            movie.title = title
            movie.imdb_ref = imdb
            for g in genres:  
                genre = Genre.objects.get(id=int(g))
                movie.genres.add(genre)

            movie.save()
            return redirect('/')

    movie_form = NewMovieForm()
    return render(request=request, template_name="userview/admin.html", context={'movie_form':movie_form})


def edit(request : HttpRequest, *args, **kwargs):
    if not request.user.is_superuser:
        return redirect('/')
    
    pk = kwargs['pk']
    if not Movie.objects.filter(pk=pk).exists():
        return render(request=request, template_name="userview/movie.html", context={'movie': False, 'id':pk})
    
    movie = Movie.objects.get(pk=pk)

    if request.method == "POST":
        form = NewMovieForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            genres = form.cleaned_data.get('genres_field')
            imdb = form.cleaned_data.get('IMDB')

            movie.title = title
            movie.imdb_ref = imdb

            movie.genres.clear()
            for g in genres:  
                genre = Genre.objects.get(id=int(g))
                movie.genres.add(genre)

            movie.save()
            return redirect('/')

    else:
        values = {
            'title': movie.title, 
            'IMDB': movie.imdb_ref,
            'genres_field': [ g.id for g in movie.genres.all()]
        }

        form = NewMovieForm(initial=values)
        return render(request=request, template_name="userview/admin.html", context={'movie_form':form})


def movie(request : HttpRequest, *args, **kwargs):
    pk = kwargs['pk']
    if not Movie.objects.filter(pk=pk).exists():
        return render(request=request, template_name="userview/movie.html", context={'movie': False, 'id':pk})
    
    movie = Movie.objects.get(pk=pk)
    comments = Comment.objects.filter(movie_id = movie.id).order_by('-id')
    ratings = Rating.objects.filter(movie_id = movie.id)
    
    if ratings.count() == 0:
        avg_rating = '---'
    else:
        avg_rating = round(mean([ r.value for r in ratings]), 2)

    context = {'movie':movie, 'avg_rating': avg_rating, 'comments': comments}

    user_rating = Rating.objects.filter(movie_id=movie.id, user_id=request.user.id)
    is_rated = False
    if not user_rating.count() == 0:
        is_rated = True
        context['rating_value'] = user_rating[0].value
    context['is_rated'] = is_rated
 
    context['comment_form'] = NewCommentForm(initial={"movie":movie.id})
    return render(request=request, template_name="userview/movie.html", context=context)


def ratings(request : HttpRequest):
    if not request.user.is_authenticated:
        return redirect('/')
    
    ratings = Rating.objects.filter(user_id=request.user.id)
    context = {}
    if ratings.count() == 0:
        context['is_empty'] = True
    else:
        context['ratings'] = ratings
    
    
    return render(request=request, template_name="userview/ratings.html", context=context)


def rate_movie(request : HttpRequest, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('/')
    
    pk = kwargs['pk']
    movie = Movie.objects.get(pk=pk)

    if request.method == "POST":
        form = RateMovieForm(request.POST)

        if form.is_valid():
            rating_value = form.cleaned_data.get('rating_value')
            rating = Rating(value=rating_value, movie=movie, user=request.user)
            rating.save()
            return redirect(f"/movie/{pk}")
    
    form = RateMovieForm()
    return render(request=request, template_name="userview/rate_movie.html", context={"rate_form" : form, "movie" : movie})


def comment_request(request : HttpRequest):
    if not request.method == "POST":
        return redirect("/")
    
    form = NewCommentForm(request.POST.copy())
    if form.is_valid():
        text = form.cleaned_data.get('text')
        movie_id = form.cleaned_data.get('movie')

        movie = Movie.objects.get(pk=movie_id)

        comment = Comment(text=text, author=request.user, movie=movie)
        # comment.author = request.user
        # comment.movie = Movie.objects.get(pk=movie)
        # comment.text = text

        comment.save()
        return redirect(f"/movie/{movie_id}")


def register_request(request : HttpRequest):

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


def login_request(request : HttpRequest):
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


def logout_request(request : HttpRequest):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    
    return redirect('/login')
