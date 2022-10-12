"""PCD URL Configuration

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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('home', views.home, name='home'),
    path('search', views.bookSearch, name='bookSearch'),
    path('profile/', views.profilePg, name='profile'),
    path('registeration', views.registerUser, name='registeration'),
    path('forgotPass', views.forgotPassword, name='forgotPassword'),
    path('verify/<auth_token>', views.verify, name='verify'),
    # path('resetPass/<auth_token>', views.verify, name='verify'),
]