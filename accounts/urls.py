
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework.routers import DefaultRouter

from .views import DoctorView , PatientView  , LoginUserView ,ResendNewOTP, PasswordResetRequestView ,VerifyOTPRequestView ,SetConfirmNewPasswordView ,doctor_rating_list, RatingViewSet   

router = DefaultRouter()
router.register(r'doctors', DoctorView)
router.register(r'patients',PatientView)
router.register(r'Ratings',RatingViewSet)



urlpatterns = [
   
    # i use the same routes for both doctor , patient 
    path('login',LoginUserView.as_view()),
    path('password-reset',PasswordResetRequestView.as_view()),
    path('verify-otp',VerifyOTPRequestView.as_view()),
    path('set-confirm-new-password',SetConfirmNewPasswordView.as_view()),
    path('resend-new-otp',ResendNewOTP.as_view()),
    # path('image/',ProfileImageView.as_view({'get': 'list'}) ,  name='profile-image')
    path('Doctor/<int:doctor_id>/Ratings/', doctor_rating_list, name='doctor-rating-list'),

] 
urlpatterns += router.urls