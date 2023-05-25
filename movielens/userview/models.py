from django.db import models
from django.conf import settings

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
    
