from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect, HttpResponse

from django.shortcuts import render
from django.views.generic import View

from wiki_quality_web import settings


class LoginView(View):
    '''
    Created on 12 de jan de 2018
    
    @author: Raphael Luiz
    '''
        
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect('/')
        
        return render(request, "index.html")
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')
    
    