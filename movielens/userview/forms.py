from typing import Any, Mapping, Optional, Type, Union
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms.utils import ErrorList
from .models import Genre


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
    

class NewMovieForm(forms.Form):

    genres = Genre.objects.all()
    CHOICES = ( (g.id, g.name) for g in genres )

    title = forms.CharField(max_length=200)
    genres_field = forms.MultipleChoiceField(choices=CHOICES, required=False)
    IMDB = forms.CharField(max_length=200, required=False)
    



class RateMovieForm(forms.Form):
    CHOICES =(
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    )
    rating_value = forms.ChoiceField(choices=CHOICES)


class NewCommentForm(forms.Form):
    text = forms.CharField(max_length=300)
    movie = forms.CharField(widget=forms.HiddenInput())


class SearchForm(forms.Form):
    movie = forms.CharField(max_length=200, required=False)
    genre = forms.CharField(max_length=200, required=False)
    CHOICES =(
        ("0", "Minimal rating"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    )
    rating = forms.ChoiceField(choices=CHOICES, required=False)