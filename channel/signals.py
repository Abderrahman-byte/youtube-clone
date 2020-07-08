from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import *

@receiver(post_save, sender=User)
def createChannel(sender, instance, created, *args, **kwargs) :
    if created :
        channel = Channel(title=instance.username, user=instance)
        channel.save()