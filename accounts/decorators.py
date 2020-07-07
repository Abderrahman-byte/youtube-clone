from django.shortcuts import redirect
from django.urls import reverse

def unauthenticated_only(view_func) :
    def wrapper(request, *args, **kwargs) :
        next = request.GET.get('next')
        if request.user.is_authenticated :
            if next is not None :
                return redirect(next)
            else : 
                return redirect(reverse('main:index'))
        else :
            return view_func(request, *args, **kwargs)

    return wrapper