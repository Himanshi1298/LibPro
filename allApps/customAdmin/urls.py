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
from . import views
from django.urls import path
urlpatterns = [
    path('customAdmin/login', views.customAdminLogin, name='adminLogin'),
    path('adminHome/', views.adminHome, name='adminHome'),
    path('adminHome/<str:appName>/<str:appModule>/', views.listDisplay, name='listDisplay'),
    path('adminHome/<str:appName>/<str:appModule>/add', views.addModel, name='addModel'),
    path('adminHome/<str:appName>/<str:appModule>/searchUser', views.userSearch, name='userSearch'),
    path('adminHome/userAccounts/userProfiles/<int:id>/<str:st>', views.userFormAll, name='userFormAll'),
    path('adminHome/userAccounts/userLinks/<int:id>/<str:st>', views.userFormAll, name='userLinkFormAll'),
]