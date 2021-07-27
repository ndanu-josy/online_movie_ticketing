from movies.models import Movie
from movies.forms import RegistrationForm
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    allMovies = Movie.objects.all()
    return render(request, 'index.html', {'allMovies':allMovies})

@login_required(login_url='/accounts/login/')
def profile(request):
   
    return render(request, 'index.html',)


def register(request):
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        
        if form.is_valid():
        
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
        return redirect('login')
    else:
        form= RegistrationForm()
    return render(request, 'registration/registration_form.html', {"form":form})     
