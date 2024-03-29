
from django.urls import path,include
from accounts.urls import doctors_router 
from .views import SessionView


doctors_router.register('sessions', SessionView,basename= 'doctor-sessions')



urlpatterns =[
    
    path('', include(doctors_router.urls)),
]