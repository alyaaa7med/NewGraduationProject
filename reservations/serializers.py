from rest_framework import serializers
from .models import Appointement
from accounts.models import Doctor , Patient , User


class AppointmentSerializer(serializers.ModelSerializer): # it has create , update , delete 

    class Meta :
        model = Appointement
        fields = '__all__'
        read_only_fields = ['state','doctor','user']

    def validate(self , data):
        # it lacks handling the conflicts between 2 appointements (start - end ) for the doctor 
            doctor_pk = self.context.get('doctor_pk')
            #  if i use the nested serializer 
            # try : 
            #     doctor = Doctor.objects.get(id = doctor_pk)
            # except :
            #     raise serializers.ValidationError({"message":"doctor does not exist , sign up first"})
            return data
        
    def create(self, validated_data):
        
        doctor_pk = self.context.get('doctor_pk')
        doctor  = Doctor.objects.get(id=doctor_pk)

        if validated_data['price'] < 99.00 :
                raise serializers.ValidationError({"message":"price must be more than 99 egp"})
        try :
            appointement = Appointement.objects.create(**validated_data,state='free',doctor= doctor)
        except :
             raise serializers.ValidationError({"message":"you have an appointment at this time , enter an other one "})
        return appointement # it is the output i see in the serializer and u can add also a message with it in the view  
      
    def update(self, instance, validated_data): # instance uses the id of the model view set 
    # check if the combination already exists for the same doctor 
        doctor_pk = self.context.get('doctor_pk')
        doctor = Doctor.objects.get(id=doctor_pk)
        
        # this combination is unique 
        if Appointement.objects.filter(day=validated_data['day'],
                                       date=validated_data['date'],
                                       start_at=validated_data['start_at'],
                                       doctor = doctor) .exists() :
        
            raise serializers.ValidationError({"message":"you have an appointment at this time , enter an other one "})

        else :
            # Update the instance with the new validated_data
            instance.day = validated_data['day']
            instance.date = validated_data['date']
            instance.start_at = validated_data['start_at']
            instance.price = validated_data['price']
            instance.save()  # Save the updated instance
            return instance
         
    
class BookAppointmentSerializer(serializers.Serializer):
    appointment_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)

    def validate(self, attrs):
        appointment_id = attrs.get('appointment_id')
        user_id = attrs.get('user_id')
        
        try:
            appointment = Appointement.objects.get(id=appointment_id)    
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise serializers.ValidationError({"message": "This User does not exist"})
        
        except Appointement.DoesNotExist:
            raise serializers.ValidationError({"message": "This appointment does not exist"})
        
        if appointment.state != 'free':
                raise serializers.ValidationError({"message": "This appointment is already booked"})
        
        return attrs





# class MyModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MyModel
#         fields = ['field1', 'field2', 'field3']

#     def validate(self, data):
#         if self.context['request'].method == 'POST':
#             # Validation specific to create (POST) method
#             if data['field1'] == data['field2']:
#                 raise serializers.ValidationError("Field1 and Field2 cannot be equal for creation")
#         elif self.context['request'].method in ['PUT', 'PATCH']:
#             # Validation specific to update (PUT/PATCH) method
#             if data['field1'] == data['field2']:
#                 raise serializers.ValidationError("Field1 and Field2 cannot be equal for update")
#         # Add additional validation logic for other methods if needed
#         return data