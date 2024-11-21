"""Import the essential package to handle Google Login."""
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter to handle social login behavior for users logging in through a third-party social provider.

    This adapter overrides the `pre_social_login` method to check if the user
    logging in via social authentication has an email that is already registered
    in the system. If the email exists, the user is redirected to the login page
    with an error message. If multiple accounts with the same email are found,
    it also raises an error and redirects.
    """

    def pre_social_login(self, request, sociallogin):
        """
        Override the pre_social_login method to handle cases where a user is trying to log in with a Google account.

        :param request: The current request object.
        :param sociallogin: The social login.
        """
        email = sociallogin.account.extra_data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                if not sociallogin.is_existing:
                    sociallogin.user = user
            except User.DoesNotExist:
                user = User.objects.create(
                    email=email,
                    username=email.split('@')[0],
                )
                sociallogin.user = user
            except User.MultipleObjectsReturned:
                messages.error(request, "An account with this email already exists. Please log in with your existing account.")
                raise ImmediateHttpResponse(HttpResponseRedirect(reverse('login')))