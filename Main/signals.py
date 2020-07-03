from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.conf import settings

import os

from Main.models import Video

@receiver(pre_save, sender=Video)
def deletePrevPoster(sender, instance, *args, **kwargs) :
    id = instance.id
    try :
        old = Video.objects.get(pk=id)
    except Video.DoesNotExist :
        return

    old_poster = old.thumbnail_url
    new_poster = instance.thumbnail_url

    if old_poster != new_poster :
        poster_path = old_poster.lstrip('/').lstrip('media').lstrip('/')
        poster_path = os.path.join(settings.MEDIA_ROOT, poster_path)
        print(poster_path, 'deleted')
        os.remove(poster_path)

@receiver(pre_delete, sender=Video)
def deleteMediaOfDeletedVideo(sender, instance, *args, **kwargs) :
    poster_url = instance.thumbnail_url
    video_url = instance.video_url

    
    poster_path = poster_url.lstrip('/').lstrip('media').lstrip('/')
    poster_path = os.path.join(settings.MEDIA_ROOT, poster_path)
    video_path = video_url.lstrip('/').lstrip('media').lstrip('/')
    video_path = os.path.join(settings.MEDIA_ROOT, video_path)
    os.remove(poster_path)
    os.remove(video_path)
    print(poster_path, 'deleted')
    print(video_path, 'deleted')