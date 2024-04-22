from rest_framework import viewsets
from .serializers import AppointmentSerializer , BookAppointmentSerializer
from .models import Appointement
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import Doctor , Patient
from django.shortcuts import redirect

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

        if instance.patient :
            return Response({"message":"this appoitment is booked by a patient"}, status= status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    def get_serializer_context(self):

        # got it from nested url doctor/1/appointement/1 
        # return {'doctor_pk': self.kwargs['doctor_pk']}
        # got it from the jwt  
        user_id = self.request.user.id
        doctor_pk = Doctor.objects.get(user=user_id).id

        return {'doctor_pk' : doctor_pk }
   


class BrowsingAppointements (APIView): # get the free appointements 

    def get (self , request , *args, **kwargs):
        doctor_pk = self.kwargs['doctor_pk']
        
        try :
            doctor_instance = Doctor.objects.get(id=doctor_pk)
            # Retrieve appointments for the given doctor_pk
            # Correct usage of .filter() not .get() to retrieve a queryset of multiple objects
        except : 
            return Response ({'message':'No doctor with this id , use a valid one or sign up first'}, status=status.HTTP_400_BAD_REQUEST)

        appointements = Appointement.objects.filter(doctor=doctor_pk, state='free')
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
            patient_id = serializer.validated_data['patient_id']
                  
            return redirect(f'../payment/checkout-session?appointment_id={appointment_id}&patient_id={patient_id}')

        except :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class PatientAppointment (APIView) :
    
        
    def get (self , request , *args, **kwargs):
        patient_pk = self.kwargs['patient_pk']
      
        try :
            patient = Patient.objects.get(id = patient_pk)
            # Retrieve appointments for the given doctor_pk
            # Correct usage of .filter() not .get() to retrieve a queryset of multiple objects
        except : 
            return Response ({'message':'No patient with this id , use a valid one or sign up first'}, status=status.HTTP_400_BAD_REQUEST)

        appointements = Appointement.objects.filter(patient=patient_pk)
        serializer = AppointmentSerializer(appointements, many=True ) # Serialize appointments data as needed
        return Response(serializer.data, status=status.HTTP_200_OK) # here i do not use the validated data , the validate method will not be executed 
        
       

        
    

# class AppointementView(APIView):
        
#     def post(self, request , *args, **kwargs):

#         doctor_pk = self.kwargs['doctor_pk']
#         serializer = AppointementSerializer(data=request.data,context={'doctor_pk': doctor_pk})
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'data':serializer.data,
#                              'message':'created'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, doctor_pk):
#         instance = MyModel.objects.get(pk=pk)
#         serializer = MyModelSerializer(instance, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk):
#         instance = MyModel.objects.get(pk=pk)
#         serializer = MyModelSerializer(instance, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         instance = MyModel.objects.get(pk=pk)
#         instance.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     def get(self , request ):
