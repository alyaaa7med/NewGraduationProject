from rest_framework import viewsets  
from .models import Doctor , Patient  ,otpcode , User  , Rating , ProfileImage
from .serializers import UserSerializer, DoctorSerializer,ResendNewOTPSerializer ,VerifyOTPRequestSerializer, PatientSerializer , LoginSerializer , PasswordResetRequestSerializer , SetConfirmNewPasswordSerializer , RatingSerializer , photoserializer , ProfileImageSerializer
from rest_framework.parsers import MultiPartParser , FormParser
from rest_framework.response import Response
from django.utils import timezone 
from rest_framework.generics import GenericAPIView
from rest_framework import status
from .utils import send_generated_otp_to_email
from rest_framework.exceptions import ValidationError
from .pagination import Pagination
from drf_spectacular.utils import extend_schema_view, extend_schema
import base64
from rest_framework import filters
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.db import connection





class UserView (viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

#  create=extend_schema(description="Create a new object", summary="Create Object"),



# @extend_schema_view(
#     create=extend_schema(description="This Endpoint is secured with jwt token"),
#     list=extend_schema(description="This Endpoint is secured with jwt token"),
#     retrieve=extend_schema(description="This Endpoint is secured with jwt token"),
#     update=extend_schema(description="This Endpoint is secured with jwt token"),
#     partial_update=extend_schema(description="This Endpoint is secured with jwt token"),
#     destroy=extend_schema(description="This Endpoint is secured with jwt token")
# )

class DoctorView(viewsets.ModelViewSet):
    queryset = Doctor.objects.all().order_by('pk')
    serializer_class = DoctorSerializer
    parser_classes = [MultiPartParser,FormParser]
    pagination_class = Pagination

    #Searching about doctor by his name 
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get('query', None)
        if query:
            queryset = queryset.filter(
                name__icontains=query
            )
        return queryset
    
    
    
    def destroy(self, request, *args, **kwargs):
        # delete method in serializer does not work so i override the destroy
        instance = self.get_object()

        # delete the user first and the profile will be handeled automatically
        instance.user.delete()

        return Response({"message": "Profile deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    

# @extend_schema_view(
#     create=extend_schema(description="This Endpoint is secured with jwt token"),
#     list=extend_schema(description="This Endpoint is secured with jwt token"),
#     retrieve=extend_schema(description="This Endpoint is secured with jwt token"),
#     update=extend_schema(description="This Endpoint is secured with jwt token"),
#     partial_update=extend_schema(description="This Endpoint is secured with jwt token"),
#     destroy=extend_schema(description="This Endpoint is secured with jwt token")
# )
class PatientView(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    parser_classes = [MultiPartParser,FormParser]
 
    def destroy(self, request, *args, **kwargs):
        # delete method in serializer does not work so i override the destroy
        instance = self.get_object()

        # delete the user first and the profile will be handeled automatically
        instance.user.delete()

        return Response({"message": "Profile deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    




class ProfileImageView(viewsets.ModelViewSet):
    
    queryset = ProfileImage.objects.all()
    serializer_class = ProfileImageSerializer

    def get_serializer_context(self):


        if 'doctor_pk' in self.kwargs:
            doctor_pk = self.kwargs['doctor_pk']
            doctor = Doctor.objects.get(pk=doctor_pk)
            user = doctor.user  

            return {'request': self.request, 'user': user}

        
        else :
            patient_pk = self.kwargs['patient_pk']
            patient = Patient.objects.get(pk=patient_pk)
            user = patient.user

            return {'request': self.request, 'user': user}
        
    def get_queryset(self):
            
        if 'doctor_pk' in self.kwargs:
            doctor_pk = self.kwargs['doctor_pk']
            doctor = Doctor.objects.get(pk=doctor_pk)
            user = doctor.user
        else :
            patient_pk = self.kwargs['patient_pk']
            patient = Patient.objects.get(pk=patient_pk)
            user = patient.user
        
        return ProfileImage.objects.filter(user=user)

   

    


# i should change GenericAPIView to APIView 
class LoginUserView(GenericAPIView):

    serializer_class=LoginSerializer

    def post(self, request):
        # print(request.user)  answer from chatgpt will work on postman 
        email = request.data.get('email')
        password = request.data.get('password')

        if not email.strip() or not password.strip():
            return Response({"message": "Both Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)


        serializer= self.serializer_class(data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK) # should be serializer.validated_data , but i get an error for representing the access_token  , refresh_token 

        except ValidationError as error:
            error_details = error.detail
            error_type = error_details.get('error_type')
            error_message = error_details.get('message')
            return Response({'message': error_message}, status=status.HTTP_401_UNAUTHORIZED)
            
class PasswordResetRequestView(GenericAPIView):

    serializer_class= PasswordResetRequestSerializer

    def post(self, request):

        email = request.data.get('email')
        if not email.strip() :
            return Response({"message": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        

        serializer=self.serializer_class(data=request.data, context={'request':request})
        try:
            serializer.is_valid(raise_exception=True)
                
            # serializer.save()  # Calls the serializer's create method as it is post method and no need for this line here 

            return Response({
                'data': serializer.data, # take the output from the validate 
                'message': 'User Verified and otp code sent successfully, go to verify it'}, status=status.HTTP_200_OK)

        except ValidationError as error:
            error_details = error.detail
            error_type = error_details.get('error_type')
            error_message = error_details.get('message')
            return Response({'message': error_message}, status=status.HTTP_404_NOT_FOUND)  

class VerifyOTPRequestView(GenericAPIView):
    
    # although i do not need serializer , i get an error to include it  ==> i think Generic is the reason
    serializer_class = VerifyOTPRequestSerializer

    def post(self, request):
       
        #  i do not use the serialzer_validated data as i do not validate data is serializer 
        passcode = request.data.get('OTPcode')
        if not passcode:
            return Response({'message': 'OTPcode is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_pass_obj = otpcode.objects.get(otp=passcode)
            # otp is found  , so check expiration 
            if user_pass_obj.otp_expires_at > timezone.now():
                user_obj = user_pass_obj.user
                return Response({'user_id': user_obj.id,  
                         'message': 'user verified successfully, so reset your password'
                           }, status=status.HTTP_200_OK)
            
            return Response({'message': 'Your OTP code expired, resend it'}, status=status.HTTP_403_FORBIDDEN)

        except otpcode.DoesNotExist:
           return Response({'message': 'Invalid OTP code'}, status=status.HTTP_400_BAD_REQUEST)
  
class SetConfirmNewPasswordView(GenericAPIView):

    serializer_class=SetConfirmNewPasswordSerializer

    def patch(self, request):
        #  check empty request 

        user_id = request.data.get('user_id')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if not password.strip() or not confirm_password.strip() or not user_id.strip():
            return Response({"message": "password ,confirm password , user_id are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            serializer= self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            # return the new hashed  password with a message 
            return Response({'data': serializer.data,
                             'message':'password resetted successfully'}, status=status.HTTP_200_OK)

        except ValidationError as error:
            error_details = error.detail
            error_type = error_details.get('error_type')
            error_message = error_details.get('message')

            if error_type == "invalid_request":
                return Response({'message': error_message}, status=status.HTTP_404_NOT_FOUND)
            
            else:
                return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)

class ResendNewOTP(GenericAPIView):
    
    serializer_class=ResendNewOTPSerializer

    def post(self, request):
        user_id=request.data.get('user_id')
        if not user_id:
            return Response({'message': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)


        try :
            user = User.objects.get(id=user_id)

        except : 
            return Response({'message': 'User not Found'}, status=status.HTTP_404_NOT_FOUND)

        email = user.email 
 
        send_generated_otp_to_email(email)

        return Response({
                    'message':'new otp code sent successfully , verify it'
                }, status=status.HTTP_200_OK)        
  


class Checkimage(GenericAPIView):
    
    serializer_class= photoserializer

    def post(self, request):
        
        serialized = self.get_serializer(data=request.data)
        try :
            serialized.is_valid(raise_exception=True)
            serialized.save()
        
            return Response(serialized.data
                , status=status.HTTP_200_OK)        
        except ValidationError as e:
            return Response({"message": e.detail}, status=status.HTTP_400_BAD_REQUEST)




class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    

#Get all Reviews for specific doctor
@api_view(['GET'])
def doctor_rating_list(request, doctor_id):
    reviews = Rating.objects.filter(doctor_id=doctor_id)
    serializer = RatingSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def test_db_connection(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            row = cursor.fetchone()
        return HttpResponse(f"Database connection test: {row[0]}")
    except Exception as e:
        return HttpResponse(f"Database connection failed: {str(e)}")