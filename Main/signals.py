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
        if settings.DEBUG :
            old_poster_path = os.path.join(settings.BASE_DIR, old_poster.lstrip('/'))
            os.remove(old_poster_path)
        else :
            # Todo : ADD A WAY TO RETREIVE MEDIA ROOT IN PRODUTION
            pass

@receiver(pre_delete, sender=Video)
def deleteMediaOfDeletedVideo(sender, instance, *args, **kwargs) :
    poster_url = instance.thumbnail_url
    video_url = instance.video_url

    if settings.DEBUG :
        poster_path = os.path.join(settings.BASE_DIR, poster_url.lstrip('/'))
        video_path = os.path.join(settings.BASE_DIR, video_url.lstrip('/'))
        os.remove(poster_path)
        os.remove(video_path)

        print(f'removed {instance.id}')
    else :
        # Todo : ADD A WAY TO RETREIVE MEDIA ROOT IN PRODUTION
        pass