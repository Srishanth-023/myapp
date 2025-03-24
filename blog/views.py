from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse
import logging
from .models import Category, Post, AboutUs
from django.core.paginator import Paginator
from .forms import ContactForm, LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding  import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail


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
            user = form.save(commit = False) # User data created
            user.set_password(form.cleaned_data['password'])
            user.save()
            # print("C'mon !")
            messages.success(request, "Registration successful, you're into our world !")
            return redirect("blog:login")
    return render(request, "blog/register.html", {'form' : form})

def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username = username, password = password)
            if user is not None:
                auth_login(request, user)
                return redirect("blog:dashboard")
                # print("LOGIN SUCCESSFUL")
    return render(request, "blog/login.html", {'form' : form})

def dashboard(request):
    blog_title = "My Posts"
    # Getting data from Post model
    all_posts = Post.objects.filter(user = request.user)

    # Pagination
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "blog/dashboard.html", {'blog_title' : blog_title, 'page_obj' : page_obj})

def user_logout(request):
    auth_logout(request)
    return redirect("blog:index")

def forgot_password(request):
    form = ForgotPasswordForm()
    if request.method == 'POST':
        # Form
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email = email)
            # Sending Email to reset PASSWORD
            token = default_token_generator.make_token(user) # Valid only once
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            domain = current_site.domain
            subject = "REQUEST EMAIL TO RESET PASSWORD"
            message = render_to_string('blog/reset_password_email.html', {
                'domain' : domain,
                'uid' : uid,
                'token' : token
            })

            send_mail(subject, message, 'noreply@sri23.com', [email])
            messages.success(request, 'Email has been sent ✅')

    return render(request, "blog/forgot_password.html", {'form' : form})

def reset_password(request, uidb64, token):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User.objects.get(pk = uid)
            except (TypeError, ValueError, User.DoesNotExist, OverflowError):
                user = None

            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been successfully reset 👍')
                return redirect('blog:login')
            else:
                messages.error(request, 'The password reset link is invalid 😶‍🌫️')

    return render(request, "blog/reset_password.html")

def new_post(request):
    categories = Category.objects.all()
    return render(request, "blog/new_post.html", {'categories' : categories})
    