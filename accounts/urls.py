
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import DoctorView , PatientView  , LoginUserView ,ResendNewOTP, PasswordResetRequestView ,VerifyOTPRequestView ,SetConfirmNewPasswordView 
router = DefaultRouter()
router.register(r'Doctors', DoctorView)
router.register(r'Patients',PatientView)


urlpatterns = [
   
    path('', include(router.urls)),
    # i use the same routes for both doctor , patient 
    path('Login/',LoginUserView.as_view()),
    path('PasswordReset/',PasswordResetRequestView.as_view()),
    path('VerifyOTP/',VerifyOTPRequestView.as_view()),
    path('SetConfirmNewPassword/',SetConfirmNewPasswordView.as_view()),
    path('ResendNewOTP/',ResendNewOTP.as_view()),
]