from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.utils import timezone
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw 
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
    qrcode             = models.ImageField(upload_to='userQr/', blank=True)
    gender             = models.CharField(max_length=45, choices=gender, default='NA')
    bio                = models.CharField(max_length=150, null=True, blank=True)
    address            = models.TextField(max_length=500, null=True, blank=True)
    DOB                = models.DateField(blank=True, null=True)
    auth_token         = models.CharField(max_length=100, null=True)
    books_issued       = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(f'192.168.29.23:800/adminHome/userAccounts/userProfiles/change/{self.user_id}/all')
        canvas = Image.new('RGB', (430,430), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr-code-{self.user_id}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qrcode.save(fname, File(buffer), save = False)
        super().save(*args, **kwargs)


class userlinks(models.Model):
    user     = models.OneToOneField(User, related_name='userlinks', on_delete=models.CASCADE)
    website  = models.URLField(max_length = 200, null=True, blank=True, default="")
    github   = models.URLField(max_length = 200, null=True, blank=True, default="")
    linkdin  = models.URLField(max_length = 200, null=True, blank=True, default="")
    twitter  = models.URLField(max_length = 200, null=True, blank=True, default="")
    
    def __str__(self):
        return str(self.user)
