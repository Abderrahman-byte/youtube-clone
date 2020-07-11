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
    profil_img = models.ImageField(default='images/users/default.png', upload_to=randomFileName)
    profil_background = models.ImageField(default='images/users/default_background.jpeg', upload_to=randomFileName)

    def save(self) :
        im = Image.open(self.profil_img.path)
        bg = Image.open(self.profil_background.path)

        if str(self.profil_img) != 'images/users/default.png' :
            im_w, im_h = im.size

            if im_w > im_h :
                im = im.crop(((im_w - im_h) / 2 , 0, (im_w + im_h) / 2, im_h))
            elif im_w < im_h :
                im = im.crop((0 , (im_h - im_w) / 2 , im_w, (im_h + im_w) / 2))

            im = im.resize((100, 100))
            im.save(self.profil_img.path)

        if str(self.profil_background) != 'images/users/default_background.jpeg' :
            bg_w, bg_h = bg.size

            if bg_w / 6.2 < bg_h and bg_h * 6.2 > bg_w :
                box = (0, (bg_h - bg_w) / 2, bg_w, (bg_h + bg_w) / 2)
                bg = bg.crop(box)
            elif bg_w / 6.2 > bg_h and bg_h * 6.2 < bg_w :
                box = ((bg_w - bg_h) / 2, 0, (bg_w + bg_h) / 2, bg_h)
                bg = bg.crop(box)

            bg = bg.resize((1600, 1600 / 6.2))
            bg.save(self.profil_background.path)

        super(Channel, self).save()