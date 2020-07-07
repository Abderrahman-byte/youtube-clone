from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.decorators import method_decorator

from .decorators import *
from .forms import *

class LoginView(View) :
    @method_decorator(unauthenticated_only)
    def get(self, request) :
        next = request.GET.get('next')
        return render(request, 'accounts/login.html', {'next': next})

    def post (self, request) :
        username = request.POST.get('username')
        password = request.POST.get('password')
        next = request.POST.get('next')
        user = authenticate(request, username=username, password=password)

        if user is not None :
            login(request, user)
            if next is not None :
                return redirect(next)
            else :
                return redirect(reverse('main:index'))

        else :
            messages.error(request, 'username or password is incorrect')
            return render(request, 'accounts/login.html', {'next': next})

class RegisterView(View) :
    @method_decorator(unauthenticated_only)
    def get(self, request) :
        next = request.GET.get('next')
        return render(request, 'accounts/register.html', {'next': next})

    def post(self, request) :
        next = request.POST.get('next')
        form = CreateUserForm(request.POST)
        
        if form.is_valid() : 
            user = form.save()
            login(request, user)

            if next is not None :
                return redirect(next)
            else :
                return redirect(reverse('main:index'))
        else :
            for error in form.errors :
                messages.error(request, form.errors.get(error)[0])
                return render(request, 'accounts/register.html', {'next': next})

def logoutView(request) :
    next = request.GET.get('next')
    if request.user.is_authenticated :
        logout(request)

    if next is not None :
        return redirect(next)
    else :
        return redirect(reverse('main:index'))