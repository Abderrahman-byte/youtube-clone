from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponse, Http404, JsonResponse
from django.views import View
from django.conf.urls.static import serve
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.middleware.csrf import get_token
from django.db import utils
from django.db.models import Q
from django.contrib import messages

import os, json, random
from uuid import uuid4

from .utils import *
from .models import *
from channel.models import *

def indexView(request) :
    return render(request, 'main/index.html')

def watchView(request) :
    try :
        id = request.GET.get('v')
        pl_id = request.GET.get('list')
        video = Video.objects.get(pk=id)
        likes = video.videoimpression_set.filter(kind=1).count()
        dislikes = video.videoimpression_set.filter(kind=-1).count()
        comments = video.comment_set.all().order_by('-created_date')
        related = getRelatedVideos(video)
        user_impr = None
        subscribed = False
        playlist = None
        get_token(request)
    except Video.DoesNotExist :
        raise Http404

    if pl_id is not None :
        try :
            pl = Playlist.objects.get(pk=pl_id)
            
            if video not in pl.videos.all() :
                return redirect(reverse('main:watch') + f'?v={id}')

            if pl.is_public or pl.creator == request.user :
                playlist = pl
            else :
                return redirect(reverse('main:watch') + f'?v={id}')
        except Playlist.DoesNotExist :
            return redirect(reverse('main:watch') + f'?v={id}')

    if request.user.is_authenticated :
        try :
            user = request.user
            user_impr = VideoImpression.objects.get(user=user, video=video)
            user_impr = user_impr.kind
            subscribed = user in [subs.user for subs in video.channel.users.all()]
        except VideoImpression.DoesNotExist :
            user_impr = None

    context = {
        'video': video, 
        'likes': likes, 
        'dislikes': dislikes, 
        'user_impr': user_impr, 
        'subscribed': subscribed, 
        'comments': comments,
        'related': related,
        'playlist': playlist
    }

    return render(request, 'main/watch.html', context)

class submitImpressionView(View) :
    def post(self, request) :
        if not request.user.is_authenticated :
            return redirect(reverse('login'))
        else:
            try :
                body = json.loads(request.body)
                id = body.get('id')
                kind = int(body.get('kind'))
                video = Video.objects.get(pk=id)
                user = request.user
                impression, created = VideoImpression.objects.get_or_create(user=user, video=video)
                impression.kind = kind
                impression.save()

                return HttpResponse(status=201)
            except Video.DoesNotExist:
                raise Http404

    def delete(self, request) :
        if not request.user.is_authenticated :
            return HttpResponseForbidden()
        else:
            try :
                body = json.loads(request.body)
                id = body.get('id')
                video = Video.objects.get(pk=id)
                user = request.user
                impression = VideoImpression.objects.get(user=user, video=video)
                impression.delete()
                
                return HttpResponse(status=202)
            except Video.DoesNotExist or VideoImpression.DoesNotExist :
                raise Http404

class ApiPlaylists(View) :
    def get(self, request) :
        if not request.user.is_authenticated :
            return redirect(reverse('login'))
        else :
            user = request.user
            playlists = user.playlist_set.all()
            playlists = [{'id': pl.id, 'title': pl.title, 'is_public': pl.is_public, 'items': [v.id for v in pl.videos.all()]} for pl in playlists]
            body = {'playlists': playlists}
            return HttpResponse(json.dumps(body))

    def put(self, request) :
        user = request.user
        try :
            body = json.loads(request.body)
            videoId = body.get('videoId')
            playlistId = body.get('playlistId')
            action = int(body.get('action'))
            video = Video.objects.get(pk=videoId)
            playlist = Playlist.objects.get(pk=playlistId)
        except Playlist.DoesNotExist or Video.DoesNotExist :
            raise Http404

        if playlist.creator == user :
            if action == 1 : playlist.videos.add(video)
            if action == -1 : playlist.videos.remove(video)
            return HttpResponse(status=201)
        else :
            return HttpResponseForbidden()

    def post(self, request) :
        user = request.user
        if not user.is_authenticated :
            return HttpResponseForbidden()
        else :
            try :
                body = json.loads(request.body)
                video = Video.objects.get(pk=body.get('videoId'))
                playlist = Playlist(title=body.get('title'), creator=user)
                if body.get('privacy') : playlist.is_public = False
                playlist.save()
                playlist.videos.add(video)
                playlist.save()
                return HttpResponse(json.dumps({'id': playlist.id}), status=201)
            except Video.DoesNotExist :
                return HttpResponse('Video Does Not Exist.', status=400)
            except utils.IntegrityError :
                return HttpResponse('Playlist name already exists.', status=400)

class ModifieView(View) :
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
            return redirect(reverse('main:watch') + f'?v={video.id}')

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
            try :
                video.save()
            except utils.IntegrityError :
                messages.error(request, 'Each video in your channel should have a unique title')
            except Exception as ex:
                messages.error(request, ex)

            return redirect(reverse('main:modifie') + f'?v={video.id}')
        else :
            return HttpResponseForbidden()
        
def deleteVideo(request) :
    video_id = request.GET.get('v') or request.POST.get('v')
    video = Video.objects.get(pk=video_id)
    if video.channel == request.user :
        video.delete() 
        return redirect(reverse('main:index'))
    else :
        return HttpResponseForbidden()

class UploadView(View) :
    def get(self, request) :
        if request.user.is_authenticated :
            return render(request, 'main/upload.html')
        else :
            messages.info(request, 'The page you requested is members only.')
            return redirect(reverse('login') + f'?next={request.path}')

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

class SubscribeView(View) :
    def post(self, request) :
        if request.user.is_authenticated :
            body = json.loads(request.body)
            channelId = body.get('channelId')
            try : 
                channel = Channel.objects.get(pk=channelId)
            except Channel.DoesNotExist :
                raise Http404

            if channel.user == request.user :
                return HttpResponseForbidden()
            else :
                s = Subscription(channel=channel.user, user=request.user)
                s.save()
                return HttpResponse(status=201)
        else :
            return HttpResponseForbidden()

    def delete(self, request):
        if request.user.is_authenticated :
            body = json.loads(request.body)
            channelId = body.get('channelId')
            try : 
                channel = Channel.objects.get(pk=channelId)
                s = Subscription.objects.get(channel=channel.user, user=request.user)
                s.delete()
                return HttpResponse(status=201)
            except Channel.DoesNotExist or Subscription.DoesNotExist :
                return Http404

        else :
            return HttpResponseForbidden()

def submitViews(request) :
    body = json.loads(request.body)
    id = body.get('id')
    try :
        video = Video.objects.get(pk=id)
        video.add_view()
        return HttpResponse(status=201)
    except Video.DoesNotExist :
        raise Http404

class ApiComments(View) :
    def post(self, request) :
        body = json.loads(request.body)
        id = body.get('id')
        content = body.get('content')

        if request.user.is_authenticated :
            try :
                video = Video.objects.get(pk=id)
                if video.allow_comments :
                    c = video.comment_set.create(user=request.user, content=content)
                    c.save()
                    data = {'id': c.id, 'content': c.content, 'user': c.user.channel.title, 'profil': c.user.channel.profil_img}
                    return JsonResponse(data)
                else :
                    return HttpResponseForbidden()
            except Video.DoesNotExist :
                raise Http404
        else :
            return HttpResponseForbidden()


    def delete(self, request) :
        body = json.loads(request.body)
        id = body.get('id')

        if request.user.is_authenticated :
            try :
                comment = Comment.objects.get(pk=id)
                if comment.user == request.user :
                    comment.delete()
                    return HttpResponse(status=201)
                else :
                    return HttpResponseForbidden()
            except Comment.DoesNotExist :
                raise Http404
        else :
            return HttpResponseForbidden()

    def put(self, request) :
        body = json.loads(request.body)
        id = body.get('id')
        content = body.get('content', '')

        if request.user.is_authenticated :
            try :
                comment = Comment.objects.get(pk=id)
                if comment.user == request.user :
                    comment.content = content
                    comment.save()
                    return HttpResponse(status=201)
                else :
                    return HttpResponseForbidden()
            except Comment.DoesNotExist :
                raise Http404
        else :
            return HttpResponseForbidden()

def staticView(request, path) :
    response = serve(request, path, document_root=settings.MEDIA_ROOT)
    response['Accept-Ranges'] = 'bytes'
    return response

class PlaylistView(View) :
    def get(self, request) :
        id = request.GET.get('id')
        try :
            playlist = Playlist.objects.get(pk=id)

            if playlist.is_public or playlist.creator == request.user :
                context = {
                    'playlist': playlist
                }

                return render(request, 'main/playlist.html', context)
            else :
                raise Http404
        except Playlist.DoesNotExist :
            raise Http404

    def post(self, request) :
        body = json.loads(request.body)
        id = body.get('id')
        title = body.get('title')
        privacy = body.get('privacy')

        try :
            playlist = Playlist.objects.get(pk=id)

            if playlist.creator == request.user :
                if title is not None : playlist.title = title
                if privacy is not None : playlist.is_public = not privacy
                playlist.save()
                return HttpResponse(status=201)
            else :
                return HttpResponseForbidden()
        except Playlist.DoesNotExist :
            raise Http404

def deletePlaylistView(request, id) :
    try :
        playlist = Playlist.objects.get(pk=id)

        if playlist.creator == request.user :
            playlist.delete()

            return redirect(reverse('channel:playlists', args=(playlist.creator.channel.id,)))
        else :
            return HttpResponseForbidden()
    except Playlist.DoesNotExist :
        raise Http404

class ChannelApiView(View) :
    def put(self, request) :
        body = json.loads(request.body)
        channelId = body.get('channelId') 
        videoId = body.get('videoId')

        try :
            channel = Channel.objects.get(pk=channelId)
            if channel.user != request.user :
                return HttpResponseForbidden()

            if videoId is not None :
                try :
                    video = Video.objects.get(pk=videoId)
                    channel.favorite_video = video
                except Video.DoesNotExist :
                    raise Http404
            else :
                channel.favorite_video = None
            channel.save()
            return HttpResponse(status=201)
        except Channel.DoesNotExist :
            raise Http404

def searchView(request) :
    query = request.GET.get('query')

    latest_video = None
    videos_results = Video.objects.filter(Q(title__icontains=query) |  Q(description__icontains=query))
    channels_results = Channel.objects.filter(Q(title__icontains=query) |  Q(about__icontains=query))

    try :
        content_type = ContentType.objects.get(name=query)
    except ContentType.DoesNotExist :
        content_type = None

    try :
        channel = Channel.objects.get(title__iexact=query)
    except Channel.DoesNotExist :
        try :
            user = User.objects.get(username__iexact=query)
            channel = user.channel
        except User.DoesNotExist :
            channel = None

    if content_type is not None :
        videos_results |= videos_results.objects.filter(content_type__iexact=content_type)

    videos_results = videos_results.order_by('-views', '-posted_date')[:10]

    for ch in channels_results :
        views = 0
        total = ch.user.video_set.count()
        for v in ch.user.video_set.all() :
            views += v.views
        av_views = views / total
        latest_video = ch.user.video_set.filter(views__gte=av_views).order_by('-posted_date')[:1]
        videos_results |= latest_video

    if channel is not None :
        views = 0
        total = channel.user.video_set.count()
        for v in channel.user.video_set.all() :
            views += v.views
        av_views = views / total
        latest_video = channel.user.video_set.filter(views__gte=av_views).order_by('-posted_date')[:2]
        videos_results |= latest_video

    if channel not in channels_results and channel is not None:
        channels_results = [*channels_results, channel] 
    
    context = {
        'query': query,
        'videos_results': videos_results,
        'channels_results': channels_results
    }

    return render(request, 'main/search.html', context)