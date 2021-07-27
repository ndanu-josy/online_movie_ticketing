from django.db import models
from cloudinary.models import CloudinaryField

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
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)

    def __str__(self):
        return self.name