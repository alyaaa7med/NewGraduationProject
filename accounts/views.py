from rest_framework import viewsets  
from .models import Doctor , Patient  ,otpcode , User
from .serializers import DoctorSerializer,ResendNewOTPSerializer ,VerifyOTPRequestSerializer, PatientSerializer , LoginSerializer , PasswordResetRequestSerializer, SetConfirmNewPasswordSerializer 
from rest_framework.parsers import MultiPartParser , FormParser
from rest_framework.response import Response
from django.utils import timezone 
from rest_framework.generics import GenericAPIView
from rest_framework import status
import base64
from .utils import send_generated_otp_to_email
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class DoctorView(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    parser_classes = [MultiPartParser,FormParser]

class PatientView(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
class LoginUserView(GenericAPIView):

    serializer_class=LoginSerializer
    def post(self, request):
        serializer= self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PasswordResetRequestView(GenericAPIView):

    serializer_class=PasswordResetRequestSerializer

    def post(self, request):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        try:
            serializer.is_valid(raise_exception=True)
            return Response({'message':'otp code sent successfully , go to verify it '}, status=status.HTTP_200_OK)

        except ValidationError : 
            return Response({'message':'user with that email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyOTPRequestView(GenericAPIView):
    
    serializer_class = VerifyOTPRequestSerializer

    def post(self, request):

        passcode = request.data.get('OTPcode')
        if not passcode:
            return Response({'message': 'OTPcode not provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_pass_obj = otpcode.objects.get(otp=passcode)
            if user_pass_obj.otp_expires_at > timezone.now():
                user_obj = user_pass_obj.user
                if user_obj:
                    user_id_str = str(user_obj.id)  # Convert user ID to string
                    uidb64 = base64.b64encode(user_id_str.encode())  # Encode the user ID to bytes
            
                    return Response({'user_id': uidb64.decode(),  
                         'message': 'user verified successfully, so reset your password'
                           }, status=status.HTTP_200_OK)
        
                return Response({'message': 'your OTP code expired, resend it'}, status=status.HTTP_401_UNAUTHORIZED)
    
            return Response({'message': 'your OTP code expired, resend it'}, status=status.HTTP_401_UNAUTHORIZED)

        except otpcode.DoesNotExist:
           return Response({'message': 'Invalid OTP code'}, status=status.HTTP_400_BAD_REQUEST)
  

class SetConfirmNewPasswordView(GenericAPIView):

    serializer_class=SetConfirmNewPasswordSerializer

    def patch(self, request):
        serializer=self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response({'data': serializer.data,
                             'message':'password resetted successfully'}, status=status.HTTP_200_OK)

        except ValidationError as error:
            error_details = error.detail
            error_type = error_details.get('error_type')
            error_message = error_details.get('message')

            if error_message[0] == "user_not_authenticated":
                return Response({'message': 'UnAuthenticated User'}, status=status.HTTP_400_BAD_REQUEST)
            elif str(error_message[0]) == "Passwords do not match.":
                return Response({'message': "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                return Response({'error': 'Credintial Error '}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ResendNewOTP(GenericAPIView):

    serializer_class=ResendNewOTPSerializer

    def post(self, request):
        try:
            uidb64=request.data.get('uidb64')
            try :
                user_id=base64.b64decode(uidb64).decode('utf-8')
            except : 
                return Response({'message': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(id=user_id)
            email = user.email 
            otp_obj = otpcode.objects.get(user_id=user_id)
            otp_obj.delete()
            send_generated_otp_to_email(email)

            return Response({
                    'message':'new otp code sent successfully , verify it'
                }, status=status.HTTP_200_OK)        
        except User.DoesNotExist:
            return Response({'message': 'User is not found.'}, status=status.HTTP_400_BAD_REQUEST)










