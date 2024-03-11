from django.contrib.auth.forms import UserChangeForm , UserCreationForm 
from .models import User 

class CustomUserCreationForm(UserCreationForm) :
    class Meta(UserCreationForm) :
        model = User
        fields = ["name","email","password","role"]
        error_class = "error"

class CustomUserChangeForm(UserChangeForm) :
    class Meta(UserChangeForm) :
        model = User
        fields = ["name","email","password","role"]
        error_class = "error"