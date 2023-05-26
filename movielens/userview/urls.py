from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("admin_view", views.admin, name="search"),
    path("ratings", views.ratings, name="ratings"),

    path("movie/<int:pk>", views.movie, name="movie"),
    path("edit/<int:pk>", views.edit, name="medit"),
    path("rate_movie/<int:pk>", views.rate_movie, name="rate_movie"),

    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("post_comment", views.comment_request, name="comment")
]