from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self):
        return self.name


# tmp to authorization
class Comment(models.Model):
    text = models.CharField(max_length=2000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    # movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateField()
    def __str__(self):
        return str(self.author) + "; " + str(self.movie.title) + "; " + str(self.text)


class Movie(models.Model):
    title = models.CharField(max_length=1000)
    genres = models.ManyToManyField(Genre)

    imdb_ref = None
    image = None

    comments = models.ManyToManyField(Comment)


    def __str__(self):
        return self.title+";    (" + "".join([str(genre)+" " for genre in self.genres.all()]) + ")"

class Rating(models.Model):
    value = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user) + " " + str(self.movie.title) + " " + str(self.value)
    
