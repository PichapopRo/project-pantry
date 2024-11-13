from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                if user and not sociallogin.is_existing:
                    messages.error(request, "An account with this email already exists. Please log in with your existing account.")
                    raise ImmediateHttpResponse(HttpResponseRedirect(reverse('login')))
            except User.MultipleObjectsReturned:
                messages.error(request, "An account with this email already exists. Please log in with your existing account.")
                raise ImmediateHttpResponse(HttpResponseRedirect(reverse('login')))

