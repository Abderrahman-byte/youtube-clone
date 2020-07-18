from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404, HttpResponseForbidden
from django.views.generic import View
from django.core.files.images import ImageFile
from django.core.files.storage import FileSystemStorage

from datetime import timedelta, time, datetime

from .models import *
from Main.utils import *

def index(request, id) :
    try :
        channel = Channel.objects.get(pk=id)
        subs = channel.user.users.all().count()
        is_subscribed = request.user in [sub.user for sub in channel.user.users.all()]
        videos = channel.user.video_set.all().order_by('-posted_date')[:4]

        for video in videos :
            t = timedelta(seconds=video.duration)
            video.duration = str(t)

        if channel.favorite_video is not None :
            f_video = channel.favorite_video
        elif channel.user.video_set.count() < 1 :
            f_video = None
        else :
            av_views = 0
            total = channel.user.video_set.count()
            for v in channel.user.video_set.all() : av_views += v.views
            av_views = av_views / total
            f_video = channel.user.video_set.filter(views__gt=av_views).order_by('-posted_date')[0]

        context = {
            'channel': channel, 
            'subs': subs, 
            'is_subscribed': is_subscribed, 
            'videos': videos, 
            'channel_index_classes': 'active',
            'f_video': f_video 
        }
        return render(request, 'channel/index.html', context)
    except Channel.DoesNotExist :
        raise Http404

class ModifieChannel(View):
    def get(self, request, id) :
        try :
            channel = Channel.objects.get(pk=id)
        except :
            raise Http404

        if request.user == channel.user :
            return render(request, 'channel/modifie.html', {'channel': channel})
        else :
            return redirect(reverse('channel:index', args=(channel.id,)))

    def post(self, request, id) :
        try :
            channel = Channel.objects.get(pk=id)
        except :
            raise Http404
        
        if request.user == channel.user :
            title = request.POST.get('title')
            about = request.POST.get('about')

            if request.FILES.get('profil-img') is not None :
                fn, ext = os.path.splitext(request.FILES.get('profil-img').name)
                fs = FileSystemStorage()
                profilImg_name = f'images/users/{generateId(30)}{ext}'
                profilImg = fs.save(profilImg_name, request.FILES.get('profil-img'))
                channel.profil_img = fs.url(profilImg)

            if request.FILES.get('background-img') is not None :
                fn, ext = os.path.splitext(request.FILES.get('background-img').name)
                fs = FileSystemStorage()
                backgroundImg_name = f'images/users/{generateId(30)}{ext}'
                backgroundImg = fs.save(backgroundImg_name, request.FILES.get('background-img'))
                channel.profil_background = fs.url(backgroundImg)

            channel.title = title
            channel.about = about
            channel.save()
            return redirect(reverse('channel:modifie', args=(channel.id,)))
        else :
            return HttpResponseForbidden()

def videosView(request, id) :
    try :
        channel = Channel.objects.get(pk=id)
        order = int(request.GET.get('order', 0))
        subs = channel.user.users.all().count()
        is_subscribed = request.user in [sub.user for sub in channel.user.users.all()]
        videos = channel.user.video_set.all()

        if order == 0 :
            videos = videos.order_by('-posted_date')
        elif order == 1 :
            videos = videos.order_by('posted_date')
        elif order == 2:
            videos = videos.order_by('-views')
        else :
            videos = videos.order_by('-posted_date')

        for video in videos :
            t = timedelta(seconds=video.duration)
            video.duration = str(t)

        context = {
            'channel': channel, 
            'subs': subs, 
            'is_subscribed': is_subscribed, 
            'videos': videos,
            'channel_videos_classes': 'active'
        }

        return render(request, 'channel/videos.html', context)
    except Channel.DoesNotExist :
        raise Http404

def playlistsView(request, id) :
    try :
        channel = Channel.objects.get(pk=id)
        subs = channel.user.users.all().count()
        is_subscribed = request.user in [sub.user for sub in channel.user.users.all()]

        if channel.user == request.user :
            playlists = channel.user.playlist_set.all 
        else :
            playlists = channel.user.playlist_set.filter(is_public=True) 

        context = {
            'channel': channel, 
            'subs': subs, 
            'is_subscribed': is_subscribed,
            'channel_playlists_classes': 'active',
            'playlists': playlists
        }

        return render(request, 'channel/playlists.html', context)
    except Channel.DoesNotExist :
        raise Http404

def aboutChannel(request, id) :
    try :
        channel = Channel.objects.get(pk=id)
        subs = channel.user.users.all().count()
        is_subscribed = request.user in [sub.user for sub in channel.user.users.all()]
        views = 0
        for v in channel.user.video_set.all() : views += v.views  

        context = {
            'channel': channel, 
            'subs': subs, 
            'is_subscribed': is_subscribed,
            'channel_about_classes': 'active',
            'views' : views
        }

        return render(request, 'channel/about.html', context)
    except Channel.DoesNotExist :
        raise Http404

def subscriptionsChannel(request, id) :
    try :
        channel = Channel.objects.get(pk=id)

        if channel.user == request.user :
            subs = [c.channel.channel for c in channel.user.channels.all()]

            context = {
                'user_channel': channel,
                'subs_channels': subs
            }
            return render(request, 'channel/subs.html', context)
        else :
            raise Http404
    except Channel.DoesNotExist :
        raise Http404