from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import SessionSerializer
from payment.models import Session

class SessionView(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    def get_serializer_context(self):
        
        # user = self.request.user
        
        return {'doctor_pk':self.kwargs.get('doctor_pk'), 
                'session' :1}
    #   
        
