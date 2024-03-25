from rest_framework import serializers
from .models import Session

class SessionSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Session
        fields = ['id','day','date','start_at','end_at','type','price']
