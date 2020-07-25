from __future__ import annotations

import uuid

from django.contrib.auth import get_user_model, login, logout

from rest_framework import viewsets, permissions, views, response
from stupidwaitinggame.serializers import ProfileSerializer, UserSerializer
from . import models

from django.conf import settings


from django.shortcuts import redirect
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from django.http import HttpRequest

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class CurrentProfileView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: HttpRequest):
        profile, _ = models.UserProfile.objects.get_or_create(user=self.request.user)
        serializer = ProfileSerializer(profile)
        return response.Response(serializer.data)

class ClickView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: HttpRequest):
        profile, _ = models.UserProfile.objects.get_or_create(user=self.request.user)

        points, next_click = profile.click()
        return response.Response({
            'points': points,
            'next_click': next_click
        })


def login_view(request):
    if not request.user.is_authenticated:
        uname = request.get_signed_cookie(settings.USER_COOKIE_NAME, default=False)

        if not uname:
            user = get_user_model().objects.create_user('u-' + str(uuid.uuid4()))
        else:
            user = get_user_model().objects.get(username=uname)
            if user is None:
                return reset_view(request)
        login(request, user)
        request.user = user

    return redirect(request.GET.get('next', '/'))

def reset_view(request):
    if request.user.is_authenticated:
        # logout the user and remote it from the database
        # this should also delete the UserProfile
        user = request.user
        logout(request)

        # find and delete the userprofile
        up = models.UserProfile.objects.filter(user=user)
        if up is not None:
            up.delete()

        # if the user is not staff, delete the user too
        if not user.is_staff:
            user.delete()

    # clear the user_cookie
    response = redirect(request.GET.get('next', '/'))
    response.delete_cookie(settings.USER_COOKIE_NAME)
    return response