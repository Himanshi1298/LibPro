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
    path('customAdmin/login/', views.customAdminLogin, name='adminLogin'),
    path('customAdmin/logout/', views.customAdminLogout, name='adminlogut'),
    path('adminHome/', views.adminHome, name='adminHome'),
    path('adminHome/<str:appName>/<str:appModule>/listDisplay', views.listDisplay, name='listDisplay'),
    path('adminHome/book/<str:appModule>/add/', views.addModel, name='addModel'),
    path('adminHome/book/<str:appModule>/<int:id>/change/', views.changeModel, name='changeModel'),
    path('adminHome/search/<str:appModule>/', views.specificSearch, name='specificSearch'),
    path('adminHome/userAccounts/userProfiles/change/<int:id>/<str:st>/', views.userFormAll, name='userFormAll'),
    path('adminHome/issueBookFor/user/<int:id>/', views.issueBookFor, name='issueBookFor'),
    path('adminHome/issueBookFor/user/<int:uid>/<int:bid>/', views.checkAndAction, name='checkAndAction'),
    path('adminHome/returnBookFor/user/<int:uid>/<int:bid>/', views.returnBookFor, name='returnBookFor'),
    path('adminHome/renewBookFor/user/<int:uid>/<int:bid>/', views.renewBookFor, name='renewBookFor'),
    path('adminHome/reserveBookFor/user/<int:uid>/<int:bid>/', views.reserBookFor, name='reserBookFor'),
    path('adminHome/delete/<str:appModule>/<int:id>/', views.deleteSpecific, name='deleteSpecific'),
]