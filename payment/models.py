from django.db import models
from accounts.models import Doctor 


class Session(models.Model):
    Session_CHOICES =[
        ('standard','Standard'),
        ('premium','Premium'),
    ] 
    State_CHOICES = [
        ('free','Free'),
        ('booked','Booked'),
    ]
    day = models.CharField(max_length=15) # ,blank = False , null = False
    date = models.DateField()
    start_at =models.TimeField() # entered by doctor 
    end_at = models.TimeField()
    type = models.CharField(max_length = 10, choices = Session_CHOICES )
    price = models.DecimalField(max_digits=10, decimal_places=2 , null = True) # add null for previous rows in db
    state = models.CharField(max_length = 10, choices = State_CHOICES , default = 'free' )
