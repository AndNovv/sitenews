"""sitenews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path
from main import views

urlpatterns = [
    path('', include('main.urls')),
    path('main/', include('main.urls')),
    path('article/', include('main.urls')),
    path('admin/', admin.site.urls),
    path('news/', views.news, name='news'),
    path('authorization/', views.authorization, name='authorization'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('changesubs/', views.changesubs, name='changesubs'),
    path('leave/', views.leave, name='leave'),
]
