from rest_framework import viewsets  
from .models import CataractDisease
from .serializers import CataractDiseaseSerializer
from rest_framework.parsers import MultiPartParser , FormParser

from accounts.models import User
class CataractDiseaseView(viewsets.ModelViewSet):
    queryset = CataractDisease.objects.all()
    serializer_class = CataractDiseaseSerializer
    parser_classes = [MultiPartParser,FormParser]

    def get_serializer_context(self):
        
        return {'request': self.request, 'user_pk': self.kwargs['user_pk']}
    

    def get_queryset(self):
            
        user_pk = self.kwargs['user_pk']
        user = User.objects.get(pk=user_pk) 

        return CataractDisease.objects.filter(user=user)