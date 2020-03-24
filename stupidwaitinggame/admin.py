from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):

    def user__username(self, obj):
        return obj.user.username
    user__username.sort_order = 'user__username'

    list_display = ['user__username', 'score', 'last_click', 'next_click']
    search_fields = ['user__username']