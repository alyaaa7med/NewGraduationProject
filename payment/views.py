from rest_framework import viewsets  
from rest_framework.response import Response
from rest_framework import status
from .models import Session
from .serializers import SessionSerializer
from django.conf import settings
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY

LocalDomain='http://127.0.0.1:8000/'
PublicDomain='https://sightsaver.onrender.com/'

class SessionView(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class =SessionSerializer

class Successview(APIView):
    
    def get(self, request):

        return Response({"message":"success"})

class Cancelview(APIView):
    
    def get(self, request):

        return Response({"message":"Canceled"})
    

class CreateCheckoutSessionView(APIView):
    
    def post(self, request, *args, **kwargs):

        patient_session_id = self.kwargs['pk']

        try:
            patient_session = Session.objects.get(id=patient_session_id)
            checkout_stripe_session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency':'egp',
                        'unit_amount':int(patient_session.price)*100,
                        'product_data':{
                            'name':patient_session.type + ' session'}
                    },
                    'quantity': 1,
                },],
                mode='payment', # as you pay one time not subscription
                success_url= PublicDomain+'payment/Success',
                cancel_url=  PublicDomain+'payment/Cancel',
               
            )

            return Response({"url": checkout_stripe_session.url})

        except Exception as e:
            # return Response({'message':'something went wrong while creating stripe session'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# webhook used to : recieve requests  from public domain to my local machine 
# stripe listen => stablish a direct connection between stripe and my localllll machine
# but in real world you should build a real webhook handler and test that your public domain recieving
# post requests from stripe but in development we use stripe listen to have those events forward 
# directly to the local machine so no need to create a stripe webhook  from a | dashboard | , stripe 
# listen => the cli is going to configure a webhook endpoint for you on stripe dashboard 
# stripe trigger command => makes an api request  to stripe that is creating the object ,then actions are taken 
# the resault in the event published in our accounts , stripes sees that we have a cli ,so those events
# will be delivered to our local machine 
        
# now : i will create my handler and make it listen to stripe using the cli as in development phase



# The @csrf_exempt decorator is used to prevent Django from performing the CSRF validation that is
# done by default for all POST requests .



@csrf_exempt
def WebhookView(request):
  
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None
  try:
    event = stripe.Webhook.construct_event(payload,sig_header,settings.STRIPE_WEBHOOK_KEY)

  except ValueError as e:
      # Invalid payload
    return HttpResponse(status=400)
  
  except stripe.error.SignatureVerificationError as e:
      # Invalid signature
    return HttpResponse(status=400)
  
  if event['type'] == 'checkout.session.completed':
    session = event['data']['object']
    
    print("here")

    if session.mode == 'payment' and session.payment_status == 'paid':
       return HttpResponse(status=200)
    else :
       return HttpResponse(status=200)
  
  else:
    print('Unhandled event type {}'.format(event['type']))
    return HttpResponse(status=200)
    return HttpResponse(status=500)

