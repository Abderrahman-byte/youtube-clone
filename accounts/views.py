from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages

class LoginView(View) :
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
    def get(self, request) :
        return render(request, 'accounts/register.html')