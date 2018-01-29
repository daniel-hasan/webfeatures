from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect, render_to_response
from django.urls.base import reverse
from django.views.generic.edit import CreateView

from wqual.views.authentication import authenticate


class SignUpView(CreateView):
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
            return redirect('home')
        else:
            form = UserCreationForm()
        return render_to_response('content/signup.html', {'form': form})