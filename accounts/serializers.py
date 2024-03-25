
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Doctor , Patient , otpcode
from django.contrib.auth.hashers import make_password
from .utils import send_generated_otp_to_email
import base64
from django.contrib.auth.hashers import check_password



User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

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

    user= UserSerializer() 
    confirm_password = serializers.CharField(write_only=True, required=True)
    class Meta : 
        model = Doctor   
        fields = ['id','user','confirm_password','phone','syndicateNo','specialization','university','work_experience','gender','image']
        

    def validate(self, data):
        if data['user']['password'] != data['confirm_password']:
            raise serializers.ValidationError("The passwords do not match.")
        return data
    
    # during deserialization                                         ______
    #  create method  will be called automatically when you make a  | POST | request to create a new Doctor object through the associated ModelViewSet
                                                                  # |______|
    def create(self, validated_data): # validated data = user + doctor 
        user_data = validated_data.pop('user') # This line extracts the nested user data from the validated data dictionary. Since user is a nested serializer field, it's removed from validated_data and stored separately in user_data.
        password = user_data.get('password')
        validated_data.pop('confirm_password') # Remove 'confirm_password' from the data

        hashed_password = make_password(password)  # Hash the password
        user_data['password'] = hashed_password

        user = User.objects.create(**user_data, role='doctor') # Here, a new User instance is created using the extracted user data (user_data). Additionally, the role attribute is set to 'doctor', indicating that this user instance represents a doctor.
        doctor = Doctor.objects.create(user=user,**validated_data)  # validated data does not have user 
        doctor.save()
        return doctor  # why not return user ? i tried it but i get an error
        
    # def update(self , validated_data):
    #     doctor_pk = self.context.get('doctor_pk')

        
    def delete(self):
        doctor_pk = self.context.get('doctor_pk')
        Doctor.objects.filter(id=doctor_pk).delete()

class PatientSerializer(serializers.ModelSerializer):
 
    user= UserSerializer() 
    confirm_password = serializers.CharField(write_only=True, required=True)
    class Meta : 
        model = Patient
        fields =['id','user','confirm_password','gender','phone','birthdate','image']

    
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
        patient.save()
        return patient
    
    # def update(self,validated_data):
    #     pass
    
    def delete(self):
        patient_pk = self.context.get('patient')
        Patient.objects.filter(id=patient_pk).delete()


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

        if email and password: # no need for this check 
            try :
                # check if the user with this email exists
                user = User.objects.get(email=email)

                if check_password(password, user.password):
                    tokens=user.tokens()  # generate access token and refresh 
                    # check if the patient or doctor to return the id in response and its type
                    try:
                        doctor = Doctor.objects.get(user=user)
                        profileid = doctor.id
                        usertype='doctor'  # user.role

                    except Doctor.DoesNotExist:
                        try :
                            patient = Patient.objects.get(user=user)
                            profileid = patient.id
                            usertype='patient'

                        except Patient.DoesNotExist:
                            # surly it is a guest
                            raise serializers.ValidationError({"error_type": "not user","message":"Invalid Email or password."})
                    # validate method should return fields of serializer 
                    return {
                    "profile_id":profileid,
                    "user_type":usertype,
                    "access_token":str(tokens.get('access')),
                    "refresh_token":str(tokens.get('refresh'))
                    }
                else :
                    # password is wrong 
                    raise serializers.ValidationError({"error_type": "not user", "message": "Invalid email or password."})
            # user with this email not found 
            except :
                raise serializers.ValidationError({"error_type": "not user", "message": "Invalid email or password."})
        

class PasswordResetRequestSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=255,write_only=True)
    user_id =serializers.CharField(max_length=15,read_only=True)

    class Meta:
        Model = User
        fields = ['email','user_id']

    def validate(self, attrs):
        
        email = attrs.get('email')
        # can be try or if 
        try :
            user = User.objects.get(email=email)
            # user_id_str = str(user.id)  # Convert user ID to string
            # user_id_bytes = user_id_str.encode('utf-8')  # Convert string to bytes using UTF-8 encoding
            # uidb64 = base64.b64encode(user_id_bytes).decode('utf-8')  # Encode the user ID to bytes
            send_generated_otp_to_email(email) 
            return {'user_id': user.id}
            # validated attributes should be return or it will raises error  i return data no need to the second line          
            # return super().validate(attrs)

        except :
            # email does not exist 
            raise serializers.ValidationError({"error_type": "email not found", "message": "No User with this email"})

    
class VerifyOTPRequestSerializer(serializers.Serializer):

    OTPcode = serializers.CharField(max_length = 6,write_only=True)

    class Meta:
        model = otpcode
        fields = ['OTPcode'] 


class SetConfirmNewPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=200)
    confirm_password = serializers.CharField(max_length=200, write_only=True)
    user_id = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'confirm_password', 'user_id']

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        try:
            user = User.objects.get(id=user_id)

            if password != confirm_password:
                raise serializers.ValidationError({"error_type": "password_mismatch", "message": "Passwords do not match."})
            
            else :
                user.set_password(password)
                user.save()
                return{
                    # "password":password => will return plain text
                    "password":user.password
                }

        except User.DoesNotExist :
            raise serializers.ValidationError({"error_type": "invalid_request", "message": "User is not found."})
        

class ResendNewOTPSerializer(serializers.Serializer):
    user_id = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['user_id']



