from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("admin_view", views.admin, name="search"),
    path("movie/<int:pk>", views.movie, name="movie"),

    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout")
]