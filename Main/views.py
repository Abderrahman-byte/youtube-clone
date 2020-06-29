from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse
from django.views import View
from django.core.files.storage import FileSystemStorage

from .utils import *
from .models import *

class UploadView(View) :
    def get(self, request) :
        return render(request, 'test/test.html')

    def post(self, request) :
        if request.user.is_authenticated and request.FILES.get('video') is not None:
            fs = FileSystemStorage()
            # Add Video to filesystem
            video_file = request.FILES.get('video')
            video_id = generateId(30)
            filename = fs.save(f'videos/{video_id}.mp4', video_file)
            video_url = fs.url(filename)

            # Make video image and thumbnail
            thumbnail_url = generateThumbnail(filename)

            return render(request, 'test/test.html', {'uploaded_file_url': video_url})
        else :
            return HttpResponseForbidden()