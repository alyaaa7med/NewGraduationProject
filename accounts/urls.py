
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import DoctorView , PatientView  , LoginUserView ,ResendNewOTP, PasswordResetRequestView ,VerifyOTPRequestView ,SetConfirmNewPasswordView 
from rest_framework_nested import routers


router = DefaultRouter()
router.register(r'doctors', DoctorView)
router.register(r'patients',PatientView)

doctors_router = routers.NestedDefaultRouter(router , 'doctors',lookup ='doctor_pk') #parent : doctors (must be the same name of the default router) ,lookup : we have doctor_pk 


urlpatterns = [
   
    path('', include(router.urls)),
    # i use the same routes for both doctor , patient 
    path('Login/',LoginUserView.as_view()),
    path('PasswordReset/',PasswordResetRequestView.as_view()),
    path('VerifyOTP/',VerifyOTPRequestView.as_view()),
    path('SetConfirmNewPassword/',SetConfirmNewPasswordView.as_view()),
    path('ResendNewOTP/',ResendNewOTP.as_view()),
]