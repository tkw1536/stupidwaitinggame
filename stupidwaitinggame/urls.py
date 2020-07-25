"""stupidwaitinggame URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name='base/home.html')), name='home'),

    path('api/1/auth/', views.login_view, name='login'),
    path('api/1/reset/', views.reset_view, name='reset'),

    path('api/1/profile/', views.CurrentProfileView.as_view()),
    path('api/1/click/', views.ClickView.as_view(), name='click'),

    # Disabled because it's not used anywhere at the moment
    # And just leads to data exposure
    # path('api/1/profiles/', views.ProfileViewSet.as_view({'get': 'list'})),

    path('api/admin/', admin.site.urls),
]
