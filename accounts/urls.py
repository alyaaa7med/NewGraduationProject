
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import DoctorView , PatientView  , LoginUserView ,ResendNewOTP, PasswordResetRequestView ,VerifyOTPRequestView ,SetConfirmNewPasswordView 
# ResendNewOTP 
router = DefaultRouter()
router.register(r'Doctor', DoctorView)
router.register(r'Patient',PatientView)


urlpatterns = [
   
    path('', include(router.urls)),
    path('Login/',LoginUserView.as_view()),
    path('PasswordReset/',PasswordResetRequestView.as_view()),
    path('VerifyOTP/',VerifyOTPRequestView.as_view()),
    path('SetConfirmNewPassword/',SetConfirmNewPasswordView.as_view()),
    path('ResendNewOTP/',ResendNewOTP.as_view()),
]