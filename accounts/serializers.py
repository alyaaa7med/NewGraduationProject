
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Doctor , Patient , otpcode  , Rating , photo , ProfileImage
from django.contrib.auth.hashers import make_password
from .utils import send_generated_otp_to_email
import base64
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken


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

   
    def update(self, instance, validated_data): # instance uses the id of the model view set 
        password =validated_data['password']
        hashed_password = make_password(password)  
        instance.name = validated_data['name']
        instance.email = validated_data['email']
        instance.password = hashed_password
      
        instance.save()  # Save the updated instance
        return instance 
  
class DoctorSerializer(serializers.ModelSerializer):

    # to handle the user data 

    user = UserSerializer() 
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Doctor   
        fields = ['id', 'user', 'confirm_password', 'phone', 'syndicateNo', 'specialization', 'university', 'work_experience', 'gender', 'avg_rating', 'no_of_ratings']

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
    
    def update (self ,instance , validated_data):
        user_data = validated_data.pop('user')
        validated_data.pop('confirm_password') 
        
        #update user 
        user_instance = instance.user  
        user_serializer = UserSerializer()
        user_serializer.update(user_instance, user_data)
            
        #update doctor 
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if hasattr(instance.user, 'profileimage') and instance.user.profileimage:
            user_profile_image = instance.user.profileimage.image
            representation['image'] = self.context['request'].build_absolute_uri(user_profile_image.url)
        else:
            representation['image'] = None
            
        return representation
    
class PatientSerializer(serializers.ModelSerializer):
 
    user= UserSerializer() 
    confirm_password = serializers.CharField(write_only=True, required=True)
    class Meta : 
        model = Patient
        fields =['id','user','confirm_password','gender','phone','birthdate']

    
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
    
    def update (self ,instance , validated_data):
        user_data = validated_data.pop('user')
        validated_data.pop('confirm_password') 
        
        #update user 
        user_instance = instance.user  
        user_serializer = UserSerializer()
        user_serializer.update(user_instance, user_data)
            
        #update patient 
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    def to_representation(self, instance):

        representation = super().to_representation(instance)
    
        # hasattr(instance.user, 'profileimage'): This checks if the user object associated with 
        # instance has an attribute named 'profileimage'. If it does, it returns True.
        # instance.user.profileimage: This checks if the profileimage attribute of the user object
        #  is not None. If it's not None, it returns True.        
        if hasattr(instance.user, 'profileimage') and instance.user.profileimage:
            user_profile_image = instance.user.profileimage.image
            representation['image'] = self.context['request'].build_absolute_uri(user_profile_image.url)
        else:
            representation['image'] = None
            
        return representation
   
  

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=155,write_only=True, min_length=6)
    password=serializers.CharField(max_length=255, write_only=True)
    access_token=serializers.CharField(max_length=255, read_only=True)
    refresh_token=serializers.CharField(max_length=255, read_only=True)
    profile_id = serializers.IntegerField(read_only=True)
    user_type = serializers.CharField(max_length=30,read_only=True)  
    user_id = serializers.IntegerField(read_only=True)  

    def validate(self, attrs):# if i return attr it has no relation with the serializer data (read_only or write_only )
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password: # no need for this check 
            try :
                # check if the user with this email exists
                user = User.objects.get(email=email)

                if check_password(password, user.password):
                    # tokens=user.tokens()  # generate access token and refresh 
                    refresh_token = RefreshToken.for_user(user)
                    access_token = str(refresh_token.access_token)


                    # check if the patient or doctor to return the id in response and its type
                    try:
                        doctor = Doctor.objects.get(user=user)
                        profileid = doctor.id
                        usertype='doctor'  # user.role
                        userid=user.id

                    except Doctor.DoesNotExist:
                        try :
                            patient = Patient.objects.get(user=user)
                            profileid = patient.id
                            usertype='patient'
                            userid=user.id

                        except Patient.DoesNotExist:
                            # surly it is a guest
                            raise serializers.ValidationError({"error_type": "not user","message":"Invalid Email or password."})
                         
                    # attrs['access_token'] = access_token
                    # attrs['refresh_token'] = str(refresh_token)
                    # attrs['profile_id'] = profileid
                    # attrs['user_type'] = usertype
                    # return attrs
                    
                    # it is used by the serializer.validated_data
                    return  {
                    "profile_id":profileid,
                    "user_type":usertype,
                    "user_id":userid,
                    "access_token":access_token, # str(tokens.get('access')),
                    "refresh_token":refresh_token # str(tokens.get('refresh'))
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

    #     no need 
    #     class Meta:
    #     Model = User
    #     fields = ['email','user_id']

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
    
    # no need
    # class Meta:
    #     model = otpcode
    #     fields = ['OTPcode'] 


class SetConfirmNewPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=200)
    confirm_password = serializers.CharField(max_length=200, write_only=True)
    user_id = serializers.CharField(min_length=1, write_only=True)
    
    # no need
    # class Meta:
    #     fields = ['password', 'confirm_password', 'user_id']

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist :
            raise serializers.ValidationError({"error_type": "invalid_request", "message": "User is not found."})
        
        if password != confirm_password:
            raise serializers.ValidationError({"error_type": "password_mismatch", "message": "Passwords do not match."})
            
        else :
            user.set_password(password)
            user.save()
            return{
                    # "password":password => will return plain text
                    "password":user.password
                }

        

class ResendNewOTPSerializer(serializers.Serializer):
    user_id = serializers.CharField(min_length=1, write_only=True)
    # no need 
    # class Meta:
    #     fields = ['user_id']


        
class RatingSerializer(serializers.ModelSerializer):
    
    patient_name = serializers.SerializerMethodField()

    def get_patient_name(self, obj):
        return obj.patient.user.name

    class Meta:
        model = Rating
        fields = ('id', 'patient', 'patient_name', 'doctor', 'stars', 'title', 'description', 'created_at')
        


class photoserializer (serializers.ModelSerializer ):
    
    class Meta :
        model = photo 
        fields = '__all__'


class ProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileImage
        fields = ['id', 'image']
    
    def create(self, validated_data):
        
        user = self.context.get('user')
        profile_image = ProfileImage.objects.create(user=user, **validated_data)

        return profile_image

 
    # no need 
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     if instance.image:
    #         representation['image'] = self.context['request'].build_absolute_uri(instance.image.url)
    #     return representation