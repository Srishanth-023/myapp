from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse
import logging
from .models import Post

# Create your views here.

# Getting data which is hard coded
# posts = [
#     {'id' : 1, 'title' : 'Post 1', 'content' : 'Content of Post 1'},
#     {'id' : 2, 'title' : 'Post 2', 'content' : 'Content of Post 2'},
#     {'id' : 3, 'title' : 'Post 3', 'content' : 'Content of Post 3'},
#     {'id' : 4, 'title' : 'Post 4', 'content' : 'Content of Post 4'},
# ]

def index(request):
    blog_title = "Latest Posts"

    # Getting data from Post model
    posts = Post.objects.all()
    return render(request, "blog/index.html", {'blog_title' : blog_title, 'posts' : posts})

def detail(request, slug):
    # Getting data from hard coded list 
    # post = next((item for item in posts if item['id'] == int(post_id)), None)
    try:
        # Getting data from Post model using post_id
        post = Post.objects.get(slug = slug)

    except Post.DoesNotExist:
        raise Http404("Post does not exist !")
    # logger = logging.getLogger("TESTING")
    # logger.debug(f"Post variable is {post}")

    return render(request, "blog/detail.html", {'post' : post})

def old_url_redirect(request):
    return redirect(reverse("blog:new_url"))

def new_url_view(request):
    return HttpResponse("This is the page of new url")