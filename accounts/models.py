from django.db import models
from django.contrib.auth.models import AbstractBaseUser  ,PermissionsMixin 
from django.utils.translation import gettext_lazy as _ 
from .managers import CustomUserManger 
import secrets 
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractBaseUser,PermissionsMixin) :
    #Limit the values the 1st is the actual will stored in the database , but the 2nd is the readable in the admin 
    ROLE_CHOICES =[
        ('doctor','Doctor'),
        ('patient','Patient'),
        ('guest','Guest')
    ] 
    name = models.CharField(max_length=200)
    email=models.EmailField(max_length=250,unique=True,blank=False,null = False) # should be unique 
    password = models.CharField(max_length=150)  # Increase the maximum length to 128 characters
    is_staff = models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)  
    role =models.CharField(max_length = 10, choices = ROLE_CHOICES ,default='guest' )


    USERNAME_FIELD= "email"
    REQUIRED_FIELDS= ["name","password"]  # required fields you need to create an account

    objects = CustomUserManger()

    # class Meta : 
    #     verbose_name = _("User")
    #     verbose_name_plural = _("Users")

    def __str__(self) :
        return self.email
    
    @property

    def get_full_name(self):
        pass 

    def tokens(self):    
        refresh = RefreshToken.for_user(self)
        return {
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        }
   


class otpcode(models.Model): 
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    otp=models.CharField(max_length=6 , default = secrets.token_hex(3)[:5])
    otp_created_at = models.DateTimeField(auto_now_add = True )
    otp_expires_at = models.DateTimeField(blank= True , null = True) # why ? 
   
    def __str__(self) :
        return self.user.email
    
class Doctor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone= models.CharField(max_length=15,unique=True)
    syndicateNo = models.CharField(max_length=15,unique=True)
    university = models.CharField(max_length=30)
    specialization = models.CharField(max_length=255)
    work_experience= models.CharField(max_length=255)
    gender= models.CharField(max_length=7,default='unknown')
    image = models.ImageField(upload_to="accounts/images/%Y/%m/%d/%H/%M/%S/") # ,default="accounts/images/carton.png"

    REQUIRED_FIELDS= ["phone","syndicateNo","university","specialization","image"]  # null = False + blank = False 

    def __str__(self) :
        return self.user.email
    
class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone= models.CharField(max_length=15,unique=True)
    birthdate = models.DateField()
    gender= models.CharField(max_length=7,default='unknown')
    image = models.ImageField(upload_to="accounts/images/%Y/%m/%d/%H/%M/%S/")# no need ,default="accounts/images/carton.png"


    REQUIRED_FIELDS= ["phone","image"]  # null = False + blank = False 


