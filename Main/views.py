from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponse, Http404
from django.views import View
from django.conf.urls.static import serve
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse

import os
from uuid import uuid4

from .utils import *
from .models import *

def indexView(request) :
    return render(request, 'main/index.html')

class ModifieViewView(View) :
    def get(self, request) :
        try :
            id = request.GET.get('v')
            video = Video.objects.get(pk=id)
        except Video.DoesNotExist :
            raise Http404
        
        if video.channel == request.user :
            types = ContentType.objects.all()
            return render(request, 'main/modifie.html', {'video': video, 'types': types})
        else :
            return HttpResponseForbidden()

    def post(self, request) :
        try :
            id = request.POST.get('id')
            video = Video.objects.get(pk=id)
        except Video.DoesNotExist :
            raise Http404

        if video.channel == request.user :
            # Get Post data
            title = request.POST.get('title')
            description = request.POST.get('description')
            content_type_id = int(request.POST.get('content_type'))
            allow_comments = True
            poster_file = request.FILES.get('poster')

            if request.POST.get('comments') == 'on' :
                allow_comments = False

            if poster_file is not None :
                fn, ext = os.path.splitext(poster_file.name)
                poster_name = f'images/thumbnails/{generateId(30)}{ext}'
                fs = FileSystemStorage()
                poster = fs.save(poster_name, poster_file)
                poster_url = fs.url(poster)
                video.thumbnail_url = poster_url

            video.title = title
            video.allow_comments = allow_comments
            if content_type_id > 0 : video.content_type = ContentType.objects.get(pk=content_type_id)
            if description != '' : video.description = description
            video.save()

            return redirect(reverse('main:modifie') + f'?v={video.id}')
        else :
            return HttpResponseForbidden()
        

class UploadView(View) :
    def get(self, request) :
        if request.user.is_authenticated :
            return render(request, 'main/upload.html')
        else :
            return HttpResponseForbidden()

    def post(self, request) :
        if request.user.is_authenticated and request.FILES.get('video') is not None:
            fs = FileSystemStorage()
            # Add Video to filesystem
            video_file = request.FILES.get('video')
            video_duration = round(float(request.POST.get('duration')))
            video_id = generateId(30)
            filename = fs.save(f'videos/{video_id}.mp4', video_file)
            video_url = fs.url(filename)

            # Make video image and thumbnail
            thumbnail_url = generateThumbnail(filename)

            # Create Video Model
            v = Video(title=str(uuid4()), 
                channel=request.user, 
                video_url=video_url, 
                thumbnail_url=thumbnail_url, 
                duration=video_duration)
            v.save()

            return redirect(reverse('main:modifie') + f'?v={v.id}')
        else :
            return HttpResponseForbidden()

def staticView(request, path) :
    response = serve(request, path, document_root=settings.MEDIA_ROOT)
    response['Accept-Ranges'] = 'bytes'
    return response