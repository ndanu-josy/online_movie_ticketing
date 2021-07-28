from django.conf.urls import include, url
from django.urls.conf import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns=[  
    url(r'^$',views.index,name='index'),
    url(r'register/',views.register, name='registration'),
    url('login/', auth_views.LoginView.as_view(), name='login'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'profile/', views.profile, name='profile'),
    url(r'movies/', views.movies, name='movies'),   
    path('movie/<id>', views.show_details, name="showDetails"),
    path('book_tickets/<id>', views.bookTicket, name="book_seat"),
    path('seats/<int:show>', views.seats, name="seats"),
    path('ticket', views.ticket, name="ticket"),
    path('tickets', views.allTickets, name="allTickets"),
   
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

