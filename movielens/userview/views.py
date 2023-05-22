from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import loader

# Create your views here.
def index(request : HttpRequest):
    
    return render(request=request, template_name="userview/index.html", context={})