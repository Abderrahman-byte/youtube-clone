from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.views.generic import View

from .models import *

def index(request, id) :
    try :
        channel = Channel.objects.get(pk=id)
        subs = channel.user.users.all().count()
        is_subscribed = request.user in [sub.user for sub in channel.user.users.all()]
        return render(request, 'channel/index.html', {'channel': channel, 'subs': subs, 'is_subscribed': is_subscribed})
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