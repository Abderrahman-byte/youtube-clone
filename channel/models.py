from django.db import models
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image
from io import BytesIO

from Main.utils import *

class Channel(models.Model) :
    id = models.TextField(primary_key=True, max_length=24, default=generateChannelId)
    title = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(max_length=1500, null=True, blank=True)
    profil_img = models.TextField(default='/media/images/users/default.png')
    profil_background = models.TextField(default='/media/images/users/default_background.jpeg')