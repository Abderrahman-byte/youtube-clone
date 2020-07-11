from django.db.models.signals import post_save, pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings

import os

from .models import *

@receiver(post_save, sender=User)
def createChannel(sender, instance, created, *args, **kwargs) :
    if created :
        channel = Channel(title=instance.username, user=instance)
        channel.save()

@receiver(pre_save, sender=Channel)
def removeUnusedImages(sender, instance, *args, **kwargs) :
    try :
        channel = Channel.objects.get(pk=instance.id)
    except Channel.DoesNotExist :
        return 

    old_profil = channel.profil_img
    new_profil = instance.profil_img
    old_bg = channel.profil_background
    new_bg = instance.profil_background

    if old_profil != '/media/images/users/default.png' and new_profil != old_profil :
        old_profil_path = old_profil.lstrip('/').lstrip('media').lstrip('/')
        old_profil_path = os.path.join(settings.MEDIA_ROOT, old_profil_path)
        os.remove(old_profil_path)

    if old_bg != '/media/images/users/default_background.jpeg' and new_bg != old_bg :
        old_bg_path = old_bg.lstrip('/').lstrip('media').lstrip('/')
        old_bg_path = os.path.join(settings.MEDIA_ROOT, old_bg_path)
        os.remove(old_bg_path)

@receiver(post_save, sender=Channel)
def removeMedia(sender, instance, *args, **kwargs) :
    profil_path = instance.profil_img.lstrip('/').lstrip('media').lstrip('/')
    bg_path = instance.profil_background.lstrip('/').lstrip('media').lstrip('/')
    profil_path = os.path.join(settings.MEDIA_ROOT, profil_path)
    bg_path = os.path.join(settings.MEDIA_ROOT, bg_path)
    os.remove(profil_path)
    os.remove(bg_path)