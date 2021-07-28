from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import User, City, Theatre, Hall, Movie, Show, Ticket
from datetime import datetime, timedelta
from django.utils.timezone import now, localtime
import random
import json
from .forms import RegistrationForm
# Create your views here.



def index(request):
 
    return render(request, 'index.html')

@login_required(login_url='/accounts/login/')
def movies(request):
    shows = Show.objects.all()
   
    return render(request, 'movies.html', {'shows':shows})

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

def show_details(request, id):
    return render(request, "show_details.html", {"show": Show.objects.get(id=id)})

def search(request):
    if request.method == 'POST':

        query = request.POST['q']

        for movie in Movie.objects.all():
            if query.lower() == movie.name.lower():

                return redirect(reverse(moviePage, kwargs={'movieName': movie.name}))
            
            else:
                continue

        return redirect(reverse(results, kwargs={'query': query}))


def results(request, query):

    results = []

    if query == 'all':
        allmovies = Movie.objects.all()
        return render(request, "searchResults.html", {'movies': allmovies})

    else:

        for movie in Movie.objects.all():
            if query.lower() in movie.name.lower():
                results.append(movie)

        if len(results) == 0:
            messages.error(request, 'Error: No such movie currently exists.')
            return redirect(reverse(error))

        else:
            return render(request, "movies/searchResults.html", {'movies': results})


def moviePage(request, movieName):
    return render(request, "movies/moviePage.html", {"movie": Movie.objects.get(name=movieName)})

def bookTicket(request, id):

    # current_city = request.user.city.name
    
    today = datetime.today()
    currentDate = today.strftime('%d %B, %Y')

    current_time = localtime().time()

    dayList = []

    for i in range(6):
        new_date = today + timedelta(days=i+1)
        dayList.append(new_date.strftime('%d %B, %Y'))

    current_movie = Movie.objects.get(id=id)
    theatres = Theatre.objects.filter(id=id)
    halls = Hall.objects.filter(theatre__id__in=theatres)
    shows = Show.objects.all()

    context={
        # "current_city": current_city,
        "movie": Movie.objects.get(id=id),
        "cities": City.objects.exclude(id=id),
        "today": currentDate,
        "dayList": dayList,
        "shows": shows
    }

    return render(request, "book_ticket.html", context)

def error(request):
    return render(request, "movies/error.html")
    
def shows(request, movie, city, day, hall):

    now = datetime.now()
    current_time = now.strftime("%H:%M")

    if city=="any":
        theatres = Theatre.objects.all()
    else:
        cityName = City.objects.get(name=city)
        theatres = Theatre.objects.filter(city=cityName)

    if hall == "any":
        halls = Hall.objects.filter(theatre__id__in=theatres)
    else:
        halls = Hall.objects.filter(hall_type=hall, theatre__id__in=theatres)

    datetime_obj = datetime.strptime(day, "%d %B, %Y")
    date = datetime_obj.date()
    movie_obj = Movie.objects.get(name=movie)
    shows = Show.objects.filter(movie=movie_obj, hall__id__in=halls, date=date)
    
    return JsonResponse([show.serialize() for show in shows], safe=False)

def seats(request, show):

    current_show = Show.objects.get(pk=show)

    return JsonResponse(current_show.seats, safe=False)

@csrf_exempt
def ticket(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        current_show = Show.objects.get(pk=data.get("show"))

        row = ''
        col = ''
        total_seats = 0

        for seat in data.get("seatList"):
            row = seat[0]
            col = seat[1:]
            current_show.seats[row][col] = 'Occupied'
            current_show.save()
            total_seats+=1

        cost = len(data.get("seatList")) * current_show.rate

        Ticket.objects.create(user=request.user, seat={'seatList':data.get("seatList")}, show=current_show, cost=cost)

        return JsonResponse({"message": "Ticket Created Successfully"}, status=201)

def allTickets(request):

    current_time = localtime().time()

    print(current_time)

    ticketsList = Ticket.objects.filter(user=request.user).order_by('-id')

    context = {
        'Tickets': ticketsList,
        'current_time': current_time,
        }

    return render(request, "movies/tickets.html", context)
