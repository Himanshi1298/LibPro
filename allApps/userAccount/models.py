from email.policy import default
from turtle import ondrag
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.utils import timezone
# Create your models here.


gender = (
    ('Male','Male'),
    ('Female', 'Female'),
    ('NA','NA'),
)

class userProfiles(models.Model):
    user               = models.OneToOneField(User, related_name='userProfile', on_delete=models.CASCADE)
    user_profile_image = models.ImageField(null=True, blank=True, upload_to="userProfileImgs/")
    phone              = models.CharField(max_length=12, null=True, blank=True)
    gender             = models.CharField(max_length=45, choices=gender, default='NA')
    bio                = models.CharField(max_length=150, null=True, blank=True)
    address            = models.TextField(max_length=500, null=True, blank=True)
    DOB                = models.DateField(blank=True, null=True)
    auth_token         = models.CharField(max_length=100, null=True)
    books_issued       = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.user)

class userlinks(models.Model):
    user     = models.OneToOneField(User, related_name='userlinks', on_delete=models.CASCADE)
    website  = models.URLField(max_length = 200, null=True, blank=True, default="")
    github   = models.URLField(max_length = 200, null=True, blank=True, default="")
    linkdin  = models.URLField(max_length = 200, null=True, blank=True, default="")
    twitter  = models.URLField(max_length = 200, null=True, blank=True, default="")
    
    def __str__(self):
        return str(self.user)
