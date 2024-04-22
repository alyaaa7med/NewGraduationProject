
from django.urls import path 
from .views import AppointementView , BrowsingAppointements , BookAppointment , PatientAppointment 
from rest_framework.routers import DefaultRouter



router2 = DefaultRouter()
router2.register(r'appointements', AppointementView, basename='appointements')


urlpatterns = router2.urls 

urlpatterns += [
    path('doctors/<int:doctor_pk>/appointments', BrowsingAppointements.as_view(), name='doctor-appointments-browsing'),
    path('book',BookAppointment.as_view()),

    # you can get patient from the request.user 
    
    path('patients/<int:patient_pk>/appointments', PatientAppointment.as_view()),
    ]




# # Create a nested router for appointments, which is nested under doctors

# doctors_router = routers.NestedSimpleRouter(router2 , r'doctors',lookup ='doctor') #parent : doctors (must be the same name of the default router) ,lookup : we have doctor_pk 
# doctors_router.register(r'appointements', AppointementView , basename='doctor-appointements')
