from django.contrib.auth import logout
from django.http.response import HttpResponseRedirect

from django.views.generic.base import View

class LogoutView(View):
    '''
    Created on 12 de jan de 2018
    
    @author: Raphael Luiz
    Faz o logout de  um usuário.
    '''
    
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')
    
    