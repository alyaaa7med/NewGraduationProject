
from django.urls import path,include
from rest_framework.routers import DefaultRouter 
from  rest_framework_nested import routers


from .views import DoctorView , PatientView  , LoginUserView ,ResendNewOTP, PasswordResetRequestView ,VerifyOTPRequestView ,SetConfirmNewPasswordView ,doctor_rating_list, RatingViewSet ,Checkimage , ProfileImageView 

router = DefaultRouter()
router.register(r'doctors', DoctorView)
router.register(r'patients',PatientView)
router.register(r'Ratings',RatingViewSet)


# Create a nested router for images under doctors and patients
doctor_router = routers.NestedSimpleRouter(router, r'doctors', lookup='doctor')
doctor_router.register(r'images', ProfileImageView, basename='doctor-image')

patient_router = routers.NestedSimpleRouter(router, r'patients', lookup='patient')
patient_router.register(r'images', ProfileImageView, basename='patient-image')


urlpatterns = [
   
    # i use the same routes for both doctor , patient 
    path('login',LoginUserView.as_view()),
    path('password-reset',PasswordResetRequestView.as_view()),
    path('verify-otp',VerifyOTPRequestView.as_view()),
    path('set-confirm-new-password',SetConfirmNewPasswordView.as_view()),
    path('resend-new-otp',ResendNewOTP.as_view()),
    path('Checkimage',Checkimage.as_view()),
    path('Doctor/<int:doctor_id>/Ratings/', doctor_rating_list, name='doctor-rating-list'),

] 
urlpatterns += router.urls + doctor_router.urls + patient_router.urls