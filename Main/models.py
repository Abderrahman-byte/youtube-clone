from django.db import models
from django.contrib.auth.models import User

from uuid import uuid4
from datetime import timedelta

from .utils import *

class ContentType(models.Model) :
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta :
        constraints = [
            models.UniqueConstraint(fields=['name',], name='unique_content_name')        
        ]

class Video(models.Model) :
    id = models.TextField(primary_key=True, max_length=11, default=generateId, editable=False)
    channel = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1500, blank=True, null=True)
    duration = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.SET_NULL, blank=True)
    allow_comments = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    # Dates 
    posted_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(auto_now=True)
    # Media
    video_url = models.CharField(max_length=500)
    thumbnail_url = models.CharField(max_length=500)

    class Meta :
        constraints = [
            models.UniqueConstraint(fields=['channel', 'title'], name='unique_videos_per_channel'),
            models.UniqueConstraint(fields=['video_url'], name='unique_videos_url'),
            models.UniqueConstraint(fields=['thumbnail_url'], name='unique_thumbnail_url'),
        ]

    def add_view(self) :
        self.views = self.views + 1 
        self.save()

    def get_duration(self) :
        return str(timedelta(seconds=self.duration))

class Playlist(models.Model) :
    id = models.TextField(primary_key=True, max_length=35, default=generetePlaylistId, editable=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1500, blank=True, null=True)
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

class Comment(models.Model) :
    id = models.UUIDField(primary_key=True, default=uuid4)
    content = models.TextField(max_length=1500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    # Dates 
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(auto_now=True) 

class VideoImpression(models.Model) :
    class Kind(models.IntegerChoices) :
        LIKE = 1
        DISLIKE = -1

    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kind = models.IntegerField(choices=Kind.choices, default=1)

    class Meta :
        constraints = [
            models.UniqueConstraint(fields=['video', 'user'], name='one_impression_foreach_user_on_a_video')
        ]

class Subscription(models.Model) :
    channel = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='channels')
    notify = models.BooleanField(default=False)

    class Meta :
        constraints = [
            models.UniqueConstraint(fields=['channel', 'user'], name='unique_subscription')
        ]