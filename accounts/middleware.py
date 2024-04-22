from django.contrib.auth import logout
from django.conf import settings
from django.shortcuts import redirect

class PreventMultipleLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated and if so, check if they have a session token stored
        if request.user.is_authenticated and 'session_token' in request.session:
            current_session_token = request.session.session_key
            previous_session_token = request.session.get('session_token')

            # If the current session token is different from the one stored, log out the user from the previous session
            if current_session_token != previous_session_token:
                logout(request)
                # Redirect user to login page with a message indicating why they were logged out
                return redirect(settings.LOGIN_URL + '?multiple_login_error=true')

        # Set session token to current session
        request.session['session_token'] = request.session.session_key

        response = self.get_response(request)

        return response
