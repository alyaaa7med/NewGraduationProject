from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .serializers import AppointmentSerializer , BookAppointmentSerializer
from .models import Appointement
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import Doctor , Patient , User
from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema_view, extend_schema

@extend_schema_view(
    create=extend_schema(description="This Endpoint is secured with jwt token"),
    list=extend_schema(description="This Endpoint is secured with jwt token"),
    retrieve=extend_schema(description="This Endpoint is secured with jwt token"),
    update=extend_schema(description="This Endpoint is secured with jwt token"),
    partial_update=extend_schema(description="This Endpoint is secured with jwt token"),
    destroy=extend_schema(description="This Endpoint is secured with jwt token")
)

# only doctor can crud his appointements 
class AppointementView(viewsets.ModelViewSet):
    # queryset = Appointement.objects.all()

    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
  
    def get_queryset(self):
        user_id = self.request.user.id
        doctor_pk = Doctor.objects.get(user=user_id).id

        return Appointement.objects.filter(doctor=doctor_pk )

   
    def destroy(self, request, *args, **kwargs):
        # delete method in serializer does not work so i override the destroy
        instance = self.get_object()
        if instance.user :
            return Response({"message":"this appoitment is booked by a patient"}, status= status.HTTP_400_BAD_REQUEST)
        
        return Response({"message":"Appointment deleted successfully "} ,status=status.HTTP_204_NO_CONTENT)
    

    def get_serializer_context(self):

        # got it from nested url doctor/1/appointement/1 
        # return {'doctor_pk': self.kwargs['doctor_pk']}
        # got it from the jwt  
        user_id = self.request.user.id
        doctor_pk = Doctor.objects.get(user=user_id).id

        return {'doctor_pk' : doctor_pk }
   


class BrowsingAppointements (APIView): # any user can  get the free appointements 

    def get (self , request , *args, **kwargs):
        doctor_id = self.kwargs['doctor_id']
        
        try :
            doctor_instance = Doctor.objects.get(id=doctor_id)
            # Retrieve appointments for the given doctor_pk
            # Correct usage of .filter() not .get() to retrieve a queryset of multiple objects
        except : 
            return Response ({'message':'No doctor with this id , use a valid one or sign up first'}, status=status.HTTP_400_BAD_REQUEST)

        appointements = Appointement.objects.filter(doctor=doctor_id, state='free')
        serializer = AppointmentSerializer(appointements, many=True ) # Serialize appointments data as needed
        return Response(serializer.data, status=status.HTTP_200_OK) # here i do not use the validated data , the validate method will not be executed 
        
       

class BookAppointment (APIView):

    serializer_class = BookAppointmentSerializer 

    def post(self, request):

        serializer= self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            # redirect him to the checkout view 
            # return 
            # xx = serializer.validated_data
            appointment_id = serializer.validated_data['appointment_id']
            user_id = serializer.validated_data['user_id']
                  
            return redirect(f'../payment/checkout-session?appointment_id={appointment_id}&user_id={user_id}')

        except :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class PatientAppointment (APIView) :
    
        
    def get (self , request , *args, **kwargs):
        user_id = self.kwargs['user_id']
      
        try :
            user = User.objects.get(id = user_id)
            # Retrieve appointments for the given doctor_pk
            # Correct usage of .filter() not .get() to retrieve a queryset of multiple objects
        except User.DoesNotExist : 
            return Response ({'message':'No user with this id , use a valid one or sign up first'}, status=status.HTTP_400_BAD_REQUEST)

        appointements = Appointement.objects.filter(user=user_id)
        serializer = AppointmentSerializer(appointements, many=True ) # Serialize appointments data as needed
        return Response(serializer.data, status=status.HTTP_200_OK) # here i do not use the validated data , the validate method will not be executed 
        
       

    