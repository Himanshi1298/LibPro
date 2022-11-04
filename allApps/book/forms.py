from importlib.metadata import files
from socket import fromshare
from .models import *
from django.forms import ModelForm, fields, widgets
from django.contrib.auth.models import User
from django import forms


class curdBookCategories(forms.ModelForm):
    class Meta:
        model = bookCategory
        fields = ['name', 'createdOn']
        widgets = {
             'name'      : forms.TextInput(attrs={'class': 'form-control', 'type': 'mobile', 'placeholder': 'Book Category'}),
             'createdOn' : forms.TextInput(attrs={'class': 'form-control', 'type': 'textarea', 'placeholder': 'Created On'}),
         }


class curdBookForm(forms.ModelForm):
    class Meta:
        model = book
        fields = ['book_title', 'book_desc', 'bookIsbn', 'about_book' , 'book_image', 'book_author', 'book_category', 'book_publication_date', 'book_quantity']
        widgets = {
             'book_title': forms.TextInput(attrs={'class': 'form-control', 'type': 'mobile', 'placeholder': 'Book Title'}),
             'book_desc': forms.TextInput(attrs={'class': 'form-control', 'type': 'textarea', 'placeholder': 'Book Description'}),
             'bookIsbn': forms.TextInput(attrs={'class': 'form-control', 'type': 'textarea', 'placeholder': 'Book ISBN'}),
             'about_book': forms.TextInput(attrs={'class': 'form-control text-area', 'type': 'textarea', 'placeholder': 'About Book'}),
             'book_author': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Author'}),
         }

class bookLoanForm(forms.ModelForm):
    class Meta:
        model = bookLoanDetail
        fields = ['user', 'book', 'issue_date', 'return_date']
        

class bookReservationForm(forms.ModelForm):
    class Meta:
        model = bookReservation
        fields = ['user', 'book', 'reservation_date']
