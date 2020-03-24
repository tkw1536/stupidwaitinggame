from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username']

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.UserProfile
        depth = 2
        fields = ['next_click', 'last_click', 'score', 'button_text', 'user']
