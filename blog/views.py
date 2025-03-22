from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse
import logging
from .models import Post, AboutUs
from django.core.paginator import Paginator
from .forms import ContactForm, RegisterForm

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
    all_posts = Post.objects.all()

    # Pagination
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "blog/index.html", {'blog_title' : blog_title, 'page_obj' : page_obj})

def detail(request, slug):
    # Getting data from hard coded list 
    # post = next((item for item in posts if item['id'] == int(post_id)), None)
    try:
        # Getting data from Post model using post_id
        post = Post.objects.get(slug = slug)
        related_posts = Post.objects.filter(category = post.category).exclude(pk = post.id)

    except Post.DoesNotExist:
        raise Http404("Post does not exist !")
    # logger = logging.getLogger("TESTING")
    # logger.debug(f"Post variable is {post}")

    return render(request, "blog/detail.html", {'post' : post, 'related_posts' : related_posts})


def old_url_redirect(request):
    return redirect(reverse("blog:new_url"))

def new_url_view(request):
    return HttpResponse("This is the page of new url")

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        logger = logging.getLogger("TESTING")
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if form.is_valid():
            logger.debug(f"Post Data is {form.cleaned_data['name']} - {form.cleaned_data['email']} - {form.cleaned_data['message']}")
            success_message = 'Your details has been recorded !'
            return render(request, "blog/contact.html", {'form' : form, 'success_message' : success_message})
        else:
            logger.debug("Form is not filled properly !")        

        return render(request, "blog/contact.html", {'form' : form, 'name' : name, 'email' : email, 'message' : message})
    
    return render(request, "blog/contact.html")

def about(request):
    about_content = AboutUs.objects.first()
    if about_content is None or not about_content.content:
        about_content = "Default content goes here... ❗"
    else:
        about_content = about_content.content
    return render(request, "blog/about.html", {'about_content' : about_content})

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save() # User data created
            print("C'mon !")
    return render(request, "blog/register.html", {'form' : form})