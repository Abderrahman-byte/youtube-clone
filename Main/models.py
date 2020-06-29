from django.db import models
from django.contrib.auth.models import User

from .utils import *

class ContentType(models.Model) :
    name = models.CharField(max_length=100)

    class Meta :
        constraints = [
            models.UniqueConstraint(fields=['name',], name='unique_content_name')        
        ]

class Video(models.Model) :
    id = models.TextField(primary_key=True, max_length=11, default=generateId, editable=False)
    channel = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=200, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.SET_NULL, blank=True)
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
            models.UniqueConstraint(fields=['channel', 'title'], name='unique_videos_per_channel')
        ]

    def add_view(self) :
        self.views = self.views + 1 

class Playlist(models.Model) :
    id = models.TextField(primary_key=True, max_length=35, default=generetePlaylistId, editable=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    is_public = models.BooleanField(default=True)
    videos = models.ManyToManyField(Video)
    views = models.IntegerField(default=0)
    # Dates 
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(auto_now=True)    

    class Meta :
        constraints = [
            models.UniqueConstraint(fields=['creator', 'title'], name='unique_playlist_per_user')
        ]

    def add_view(self) :
        self.views = self.views + 1 