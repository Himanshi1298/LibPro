from .models import *
from django.forms import ModelForm, fields, widgets
from django.contrib.auth .forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class userProfileForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Confirm Password'}),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'First Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Email'})
        }


class extendedProfileForm(forms.ModelForm):
    class Meta:
        model = userProfiles
        fields = ['phone', 'address', 'bio', 'user_profile_image']
        widgets = {
             'phone': forms.TextInput(attrs={'class': 'form-control', 'type': 'mobile', 'placeholder': 'Phone'}),
             'address': forms.EmailInput(attrs={'class': 'form-control', 'type': 'textarea', 'placeholder': 'Address'}),
             'bio': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Bio...'}),
         }

class userLinksForm(forms.ModelForm):
    class Meta:
        model = userlinks
        fields = ['website', 'github', 'linkdin', 'twitter']
        widgets = {
            'website': forms.TextInput(attrs={'class': 'form-control', 'type': 'url', 'placeholder': 'Website'}),
            'github': forms.TextInput(attrs={'class': 'form-control', 'type': 'url', 'placeholder': 'Github'}),
            'linkdin': forms.TextInput(attrs={'class': 'form-control', 'type': 'url', 'placeholder': 'Linkdin'}),
            'twitter': forms.TextInput(attrs={'class': 'form-control', 'type': 'url', 'placeholder': 'Twitter'}),
        }