from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import redirect, render_to_response, render
from django.views.generic.edit import CreateView


class SignUpView(CreateView):
    '''
    Created on 25 de jan de 2018
    
    @author: Raphael Luiz
    Cria um novo usuário.
    '''
    
    form_class = UserCreationForm
    template_name = 'content/signup.html'
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        return render(request, self.template_name, {'form': form})
