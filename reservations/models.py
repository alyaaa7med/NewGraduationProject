from django.db import models
from accounts.models import Doctor , User


class Appointement (models.Model):
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
    start_at =models.TimeField()
    end_at = models.TimeField()
    session_length=models.DurationField(null = True)
    type = models.CharField(max_length = 10, choices = Session_CHOICES )
    price = models.DecimalField(max_digits=10, decimal_places=2, null = True) # add null for previous rows in db
    state = models.CharField(max_length = 10, choices = State_CHOICES , default = 'free' )
    # doctor = models.ManyToManyField(Doctor) i think it may help if the admin is the person who registers  # By default, Django does not cascade delete related objects for ManyToManyField. Therefore, deleting a Doctor won't automatically delete associated Appointment instances.
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE , null = True) # i put null because of the existing database rows
    user = models.ForeignKey(User , on_delete = models.SET_NULL , null =True )


    REQUIRED_FIELDS= ["day","date","start_at","end_at","type","price","state"] 
    
    class Meta : 
        unique_together = ('day', 'date','start_at','end_at','doctor') # unique session time for the same doctor 


    def __str__(self) :
        # try :
        #     return str(self.id )
        # except :
            return str(self.id)