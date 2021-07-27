from django.db import models
from cloudinary.models import CloudinaryField
from datetime import date
import datetime as dt
# Create your models here.


class Theatre(models.Model):
    city_choice=(
        ('NAIROBI','nairobi'),
        ('KISUMU','Kisumu'),
        ('MOMBASA','Mombasa'),
        
    )
    name = models.CharField(max_length=50,null=False,default="Waves Cinema")
    city = models.CharField(max_length=20,choices=city_choice,null=False)
    address = models.CharField(max_length=30)

    def __str__(self):
        return self.name+"-"+self.address+"-"+self.city

class Hall(models.Model):

    HALL_TYPES = [
    ('2D', '2D'),
    ('3D', '3D'),
    ('4DX', '4DX'),
    ('IMAX', 'IMAX'),
    ]

    name = models.CharField(max_length=30)
    hall_type = models.CharField(max_length=4, choices=HALL_TYPES)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)

class Movie(models.Model):
    name = models.CharField(max_length=30)
    poster = CloudinaryField('imageposter')
    description = models.CharField(max_length=500)
    trailer = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Show(models.Model):
    HOUR_CHOICES = [(dt.time(hour=x), f'{y}') for x,y in [ (9, '9:00 AM'), (12, '12:00 PM'), (15, '3:00 PM'), (18, '6:00 PM'), (21, '9:00 PM')]]

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE,null=True,blank=True)
    screen = models.IntegerField(default=1)
    date = models.DateField()
    time = models.TimeField(choices=HOUR_CHOICES)
    rate = models.IntegerField()


    def __str__(self):
        return str(self.movie) + "-" + str(self.theatre) + "-" + str(self.date) + "-" + str(self.time)
