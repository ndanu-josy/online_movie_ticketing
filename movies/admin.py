from django.contrib import admin
from .models import  Theatre, Hall, Movie

# Register your models here.
admin.site.register(Hall)
admin.site.register(Movie)
admin.site.register(Theatre)