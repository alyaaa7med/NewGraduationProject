from rest_framework import serializers
from .models import CataractDisease
from .dl_model.predict import image_prediction_pipeline
from django.contrib.auth import get_user_model

User = get_user_model()

class CataractDiseaseSerializer (serializers.ModelSerializer):
    
    class Meta:
        model = CataractDisease
        fields = ['id','retina_image','result','percentage']
        read_only_fields = ['result', 'percentage']  
    

    def create(self, validated_data):

        
        user_pk = self.context.get('user_pk')
        user  = User.objects.get(id=user_pk)
        cataract_retina = CataractDisease.objects.create(**validated_data,user=user)
        cataract_retina.save()
        
        result ,percentage = image_prediction_pipeline(cataract_retina.retina_image.path) 
        cataract_retina.result = result
        cataract_retina.percentage = percentage
        cataract_retina.save()
        
        return cataract_retina


    def to_representation(self, instance):
        
        representation = super().to_representation(instance)

        retina_image = instance.retina_image
        representation['retina_image'] = self.context['request'].build_absolute_uri(retina_image.url)
 
        return representation
    
    