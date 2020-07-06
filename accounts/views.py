from django.shortcuts import render
from django.views.generic import View

class LoginView(View) :
    def get(self, request) :
        return render(request, 'accounts/login.html')