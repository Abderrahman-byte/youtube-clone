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
        context = {'channel': channel, 'subs': subs, 'is_subscribed': is_subscribed, 'videos': videos}
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
