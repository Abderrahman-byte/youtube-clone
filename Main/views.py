from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponse, Http404
from django.views import View
from django.conf.urls.static import serve
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse

from uuid import uuid4

from .utils import *
from .models import *

def indexView(request) :
    return render(request, 'main/index.html')

class ModifieViewView(View) :
    def get(self, request, id) :
        try :
            video = Video.objects.get(pk=id)
        except Video.DoesNotExist :
            raise Http404
        
        if video.channel == request.user :
            return render(request, 'main/modifie.html', {'video': video})
        else :
            return HttpResponseForbidden()


class UploadView(View) :
    def get(self, request) :
        if request.user.is_authenticated :
            return render(request, 'main/upload.html')

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

            return redirect(reverse('main:modifie', args=(v.id,)))
        else :
            return HttpResponseForbidden()

def staticView(request, path) :
    response = serve(request, path, document_root=settings.MEDIA_ROOT)
    response['Accept-Ranges'] = 'bytes'
    return response