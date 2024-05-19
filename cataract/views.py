from rest_framework import viewsets  
from .models import CataractDisease
from .serializers import CataractDiseaseSerializer
from rest_framework.parsers import MultiPartParser , FormParser

class CataractDiseaseView(viewsets.ModelViewSet):
    queryset = CataractDisease.objects.all()
    serializer_class = CataractDiseaseSerializer
    parser_classes = [MultiPartParser,FormParser]

    def get_serializer_context(self):
        
        return {'user_pk': self.kwargs['user_pk']}
    
