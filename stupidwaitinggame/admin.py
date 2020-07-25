from django.contrib import admin
from .models import UserProfile

from django.contrib.admin import SimpleListFilter
from django.utils import timezone

class InactiveFilter(SimpleListFilter):
    title = 'Activity'
    parameter_name = 'inactive'

    def lookups(self, request, model_admin):
        return [['0-points', 'No points'], ['last-click-4-weeks', 'Clicked more than four weeks ago']]

    def queryset(self, request, queryset):
        if self.value() == '0-points':
            return queryset.filter(score=0)
        elif self.value() == 'last-click-4-weeks':
            # sessions where the last click was more than 4 weeks ago
            one_month_ago = timezone.now() - timezone.timedelta(weeks=4)
            return queryset.filter(last_click__lt=one_month_ago)
        else:
            return queryset


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):

    def user__username(self, obj):
        return obj.user.username
    user__username.sort_order = 'user__username'

    list_display = ['user__username', 'score', 'last_click', 'next_click']
    list_filter = [InactiveFilter,]
    search_fields = ['user__username']