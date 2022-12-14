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
from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:id>/<str:bookName>', views.bookDetailPg, name = 'bookDetails'),
    path('book/return/<int:id>', views.returnBook, name = 'returnBook'),
    path('book/renew/<int:id>', views.renewBook, name = 'renewBook'),
    path('book/reserve/<int:id>', views.reserveBook, name = 'reserveBook'),
    path('book/checkOut/<int:id>', views.checkOut, name = 'checkOut'),
]