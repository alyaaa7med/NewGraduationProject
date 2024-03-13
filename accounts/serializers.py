
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Doctor , Patient , otpcode
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from .utils import send_generated_otp_to_email
import base64
import binascii
from django.contrib.auth.hashers import check_password



User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','name','email','password'] 

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def delete(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        user.set_password(password)
        user.delete()
        return user

    
class DoctorSerializer(serializers.ModelSerializer):

    # to handle the user data 

    user= CreateUserSerializer() 
    confirm_password = serializers.CharField(write_only=True, required=True)
    class Meta : 
        model = Doctor   
        fields = ['id','user','confirm_password','phone','syndicateNo','specialization','university','work_experience','gender','image']
        

    def validate(self, data):
        if data['user']['password'] != data['confirm_password']:
            raise serializers.ValidationError("The passwords do not match.")
        return data
    
    # during deserialization 
    def create(self, validated_data): # validated data = user + doctor 
        user_data = validated_data.pop('user') # This line extracts the nested user data from the validated data dictionary. Since user is a nested serializer field, it's removed from validated_data and stored separately in user_data.
        password = user_data.get('password')
        validated_data.pop('confirm_password') # Remove 'confirm_password' from the data

        hashed_password = make_password(password)  # Hash the password
        user_data['password'] = hashed_password

        user = User.objects.create(**user_data, role='doctor') # Here, a new User instance is created using the extracted user data (user_data). Additionally, the role attribute is set to 'doctor', indicating that this user instance represents a doctor.
        doctor = Doctor.objects.create(user=user,**validated_data)  # validated data does not have user 
        return doctor
    
    
class PatientSerializer(serializers.ModelSerializer):
 
    user= CreateUserSerializer() 
    confirm_password = serializers.CharField(write_only=True, required=True)
    class Meta : 
        model = Patient
        fields =['id','user','confirm_password','gender','birthdate']

    
    def validate(self, data):
        if data['user']['password'] != data['confirm_password']:
            raise serializers.ValidationError("The passwords do not match.")
        return data

    def create(self, validated_data): 
        user_data = validated_data.pop('user') 
        password = user_data.get('password')
        validated_data.pop('confirm_password') # Remove 'confirm_password' from the data
        
        hashed_password = make_password(password)  # Hash the password
        user_data['password'] = hashed_password
        
        user = User.objects.create(**user_data, role='patient')
        patient = Patient.objects.create(user=user,**validated_data) 
        return patient


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=155,write_only=True, min_length=6)
    password=serializers.CharField(max_length=255, write_only=True)
    access_token=serializers.CharField(max_length=255, read_only=True)
    refresh_token=serializers.CharField(max_length=255, read_only=True)
    profile_id = serializers.IntegerField(read_only=True)
    user_type = serializers.CharField(max_length=30,read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'access_token', 'refresh_token','profile_id','user_type']

    

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            try :
                user = User.objects.get(email=email)
                if check_password(password, user.password):
                    tokens=user.tokens()  # generate access token and refresh 
                    # check if the patient or doctor to return the id in response and its type
                    try:
                        doctor = Doctor.objects.get(user=user)
                        profileid = doctor.id
                        usertype='doctor'

                    except Doctor.DoesNotExist:
                        try :
                            patient = Patient.objects.get(user=user)
                            profileid = patient.id
                            usertype='patient'

                        except Patient.DoesNotExist:
                            raise serializers.ValidationError("Invalid username or password.")
                 
                    return {
                    "profile_id":profileid,
                    "user_type":usertype,
                    "access_token":str(tokens.get('access')),
                    "refresh_token":str(tokens.get('refresh'))
                    }
            except :
                raise serializers.ValidationError("Invalid username or password.")
        else:
            raise serializers.ValidationError("Both username and password are required.")
       

class PasswordResetRequestSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        
        email = attrs.get('email')

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with that email does not exist.")

        else :
            send_generated_otp_to_email(email)            

        return super().validate(attrs)
    
     
class VerifyOTPRequestSerializer(serializers.Serializer):

    OTPcode = serializers.CharField(max_length = 10)

    class Meta:
        model = otpcode
        fields = ['OTPcode']


class SetConfirmNewPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=200)
    confirm_password = serializers.CharField(max_length=200, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'confirm_password', 'uidb64']

    def validate(self, attrs):
        uidb64 = attrs.get('uidb64')
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        try:
            try :
                # if it fail while decoding 
                user_id = base64.urlsafe_b64decode(uidb64).decode('utf-8')
                user = User.objects.get(id=user_id)
            except :
                raise serializers.ValidationError({"error_type": "invalid_request", "message": "UnAuthenticated User."})

            if password != confirm_password:
                raise serializers.ValidationError({"error_type": "password_mismatch", "message": "Passwords do not match."})
            
            else :
                user.set_password(password)
                user.save()
                return user

        except User.DoesNotExist :
            raise serializers.ValidationError({"error_type": "invalid_request", "message": "UnAuthenticated User."})
        

class ResendNewOTPSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['uidb64']



