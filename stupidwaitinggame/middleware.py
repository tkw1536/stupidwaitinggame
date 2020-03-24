from django.conf import settings

from django.shortcuts import redirect

class SetUserCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user and not request.user.is_anonymous:

            if not request.get_signed_cookie(settings.USER_COOKIE_NAME, default=False):
                three_years = 3 * 365 * 24 * 60 * 60
                response.set_signed_cookie(settings.USER_COOKIE_NAME, request.user.username, max_age=three_years, path='/', secure=None, httponly=True, samesite='Strict')


        return response