from django.db import models
from django.contrib.auth.models import user

from .utils import *

class Video(models.Model) :
    id = models.TextField(primary_key=True, max_length=11, default=generateId, editable=False)
    channel = models.Foreignkey(User, on_delete=models.CASCADE)
    title = models.charField(max_length=200)
    description = models.TextField(max_length=200, blank=True, null=True)
    allow_comments = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    # Dates 
    posted_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(auto_now=True)
    # Media
    ## content = 
    ## Thumbnail = 

    class Meta :
        constraints = [
            models.UniqueConstraint(fields=('channel', 'tilte'), 'unique_videos_per_channel')
        ]


