from django.urls import reverse
from django.shortcuts import redirect

# Middleware --> Redirecting User
class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Checking for user authentication
        if request.user.is_authenticated:
            paths_to_redirect = [reverse('blog:login'), reverse('blog:register')]
            # Redirecting user
            if request.path in paths_to_redirect:
                return redirect(reverse('blog:index'))
            
        response = self.get_response(request) # It goes to next Middleware or View function
        return response

# Middleware --> Restricting User
class RestrictUnauthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        restricted_paths = [reverse('blog:dashboard')]
        # Checking for user authenticationn and Redirecting user
        if not request.user.is_authenticated and request.path in restricted_paths:
                return redirect(reverse('blog:login'))
            
        response = self.get_response(request) # It goes to next Middleware or View function
        return response