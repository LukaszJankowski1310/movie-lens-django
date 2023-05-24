from django.contrib import admin
from .models import Rating, Genre, Movie, Comment, Image

# Register your models here.
admin.site.register(Rating)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Comment)
admin.site.register(Image)