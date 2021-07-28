from django.contrib import admin
from .models import  City, Hall, Movie, Show, Theatre, Ticket

# Register your models here.


admin.site.register(Theatre)
admin.site.register(Show)
admin.site.register(Ticket)
admin.site.register(Movie)
admin.site.register(City)
admin.site.register(Hall)