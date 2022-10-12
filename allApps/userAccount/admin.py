import imp
from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(userProfiles)
class userProfiles(admin.ModelAdmin):
    list_display = ("user", "phone","books_issued")


@admin.register(userlinks)
class userlinks(admin.ModelAdmin):
    list_display = ("user", "website", "github", "linkdin", "twitter")