from django.shortcuts import render
from django.http import Http404

from .models import *

def index(request, id) :
    try :
        channel = Channel.objects.get(pk=id)
        subs = channel.user.users.all().count()
        is_subscribed = request.user in channel.user.users.all()
        return render(request, 'channel/index.html', {'channel': channel, 'subs': subs, 'is_subscribed': is_subscribed})
    except Channel.DoesNotExist :
        raise Http404