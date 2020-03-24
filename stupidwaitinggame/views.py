from __future__ import annotations

import uuid

from django.contrib.auth import get_user_model, login

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
        serializer = ProfileSerializer(self.request.user.profile)
        return response.Response(serializer.data)

class ClickView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: HttpRequest):
        profile = self.request.user.profile

        points, next_click = profile.click()
        return response.Response({
            'points': points,
            'next_click': next_click
        })


def login_view(request):
    if request.user.is_authenticated:
        return redirect(request.GET.get('next', '/'))
    
    else:
        uname = request.get_signed_cookie(settings.USER_COOKIE_NAME, default=False)

        if not uname:
            user = get_user_model().objects.create_user('u-' + str(uuid.uuid4()))
            models.UserProfile(user=user).save()
        else:
            user = get_user_model().objects.get(username=uname)

        login(request, user)

        return redirect(request.GET.get('next', '/'))