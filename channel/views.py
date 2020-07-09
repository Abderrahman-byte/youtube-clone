from django.shortcuts import render
from django.http import Http404
from .models import *

def index(request, id) :
    try :
        channel = Channel.objects.get(pk=id)
        return render(request, 'channel/index.html', {'channel': channel})
    except Channel.DoesNotExist :
        raise Http404