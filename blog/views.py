from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.

def index(request):
    return HttpResponse("Hello World, You're at blog's index")

def detail(request, post_id):
    return HttpResponse(f"This is the post's detail page and the ID is {post_id}")

def old_url_redirect(request):
    return redirect(reverse("blog:new_url"))

def new_url_view(request):
    return HttpResponse("This is the page of new url")