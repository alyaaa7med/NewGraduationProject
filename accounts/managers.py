from django.contrib.auth.base_user import BaseUserManager 
from django.core.exceptions import ValidationError 
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _ 
from django.contrib.auth.hashers import make_password


# customize user manager 
class CustomUserManger(BaseUserManager):
    
    def email_validator(self,email) :
        try :
            validate_email(email)
        except ValidationError : 
            raise ValueError(_("you must provide a valid email "))
        
    def create_user(self , name,email,password,**extra_fields):
        if not name : 
            raise ValueError (_("user must submit a  name "))
        
        if email :
            email = self.normalize_email(email)
            self.email_validator(email)
        else :
            raise ValueError(_("Base User and Email is required "))
        
        user = self.model(
            name = name,
            email = email ,
            **extra_fields 
        )

        user.password = make_password(password) 
        extra_fields.setdefault("is_staff",False)
        extra_fields.setdefault("is_superuser",False)
        user.save(using=self._db)
        return user

    
    def create_superuser(self , name,email,password,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active",True)

        if extra_fields.get("is_superuser") is not True :
            raise ValueError (_("superuser must have is_superuser = True "))
        
        if extra_fields.get("is_staff") is not True :
            raise ValueError (_("superuser must have is_staff = True "))
        
        if not password : 
            raise ValueError(_("superusers must have password"))
        

        if email :
            email = self.normalize_email(email)
            self.email_validator(email)
        else :
            raise ValueError(_("Admin User and Email is required "))
        
        user = self.create_user(name,email,password,**extra_fields)

        user.save()
        return user 
