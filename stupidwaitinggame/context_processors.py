# main/context_processors.py
from django.conf import settings

def tracking_and_legal(request):
    kwargs = {
        'include_tracking': settings.DJANGO_INCLUDE_TRACKING,
    }
    return kwargs