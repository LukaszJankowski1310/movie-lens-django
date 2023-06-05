from django.db import models
from django.conf import settings
from numpy import dot
from numpy.linalg import norm

class Genre(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=1000)
    genres = models.ManyToManyField(Genre)
    
    #IMDB cross reference
    imdb_ref = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.title+";    (" + "".join([str(genre)+" " for genre in self.genres.all()]) + ")"
    

class Comment(models.Model):
    text = models.CharField(max_length=2000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.author) + "; " + str(self.movie.title) + "; " + str(self.text)

class Image(models.Model):
    #sciezka do pliku
    path = models.CharField(max_length=200)
    isFrontImage = models.BooleanField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)



class Rating(models.Model):
    value = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user) + " " + str(self.movie.title) + " " + str(self.value)
    
def get_similar_movies(movie_id, threshold, limit):
   
    mov1 = get_vector(movie_id)
    
    results = []
    movies = Movie.objects.all()

    for movie in movies:
        if movie.id == movie_id:
            continue

        vec = get_vector(movie.id)

        sim = cosine_sim(mov1, vec)

        if sim >= threshold:
            results.append(movie)

            if len(results) >= limit:
                break
        
    return results

def get_vector(movie_id):
    movie = Movie.objects.get(pk=movie_id)
    genres = movie.genres.all()

    genres_all = Genre.objects.all()

    vec = [ 0] * len(genres_all)

    for g in genres_all:
        if g in genres:
            vec[g.id-1] = 1
    return vec

def cosine_sim(vec1, vec2):
    return round(dot(vec1, vec2)/(norm(vec1)*norm(vec2)), 2)


    

def get_most_liked_movies(limit=10):
    ratings = Rating.objects.order_by("-id")[:200] # 200 statnich ocen


    ratings = list(ratings)
    ratings.sort(key= lambda x: x.value, reverse=True)

    return ratings[:limit]

   



    

    
