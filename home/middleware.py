# middleware.py

from django.shortcuts import redirect
from django.urls import reverse

class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Redirect to the home page if authenticated
            return redirect(reverse('index'))  # Update 'home' with the actual name of your home page URL

        response = self.get_response(request)
        return response
