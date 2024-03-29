from payment.models import Session
from rest_framework import serializers

class SessionSerializer(serializers.ModelSerializer):

    class Meta :
        model = Session
        fields = ['id','day','date','start_at','end_at','type','price','state','doctor','patient']

    # def create(self, validated_data): 
