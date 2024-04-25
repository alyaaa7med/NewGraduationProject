from rest_framework.response import Response
from rest_framework import status
from reservations.models import Appointement
from django.conf import settings
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import redirect
import stripe
from accounts.models import Patient , User


stripe.api_key = settings.STRIPE_SECRET_KEY

Local='http://127.0.0.1:8000/'
PublicDomain='https://sightsaver.onrender.com/'


class Successview(APIView):
    
    def get(self, request): # id of the appointment 

        return Response({"message":"thanks for dealing with us, check your notification "})

class Cancelview(APIView): 
    
    def get(self, request):

        return Response({"message":"canceled"})
    

class CreateCheckoutSessionView(APIView):
    
    def get(self, request ):
        # url parameter 
        
        appointment_id = int(request.GET.get('appointment_id'))
        user_id = int(request.GET.get('user_id'))

        try:
            Appointment_instance = Appointement.objects.get(id = appointment_id )

            checkout_stripe_session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency':'egp',
                        'unit_amount':int(Appointment_instance.price )*100,
                        'product_data':{
                            'name':Appointment_instance.type + ' session'}
                    },
                    'quantity': 1,
                },],
                mode='payment', # as you pay one time not subscription
                success_url= PublicDomain+'payment/success', #/{{patient_session}} no need now 
                cancel_url=  PublicDomain+'payment/cancel', # may change accourding to flutter 
                metadata = {'user_id':user_id , 'appointment_id':appointment_id } # payment_intent_data.metadata
            )
            
            return redirect ( checkout_stripe_session.url)

        except :
            return Response({'message':'something went wrong while creating stripe session'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# webhook used to : recieve requests from public domain to my local machine 
# stripe listen => stablish a direct connection between stripe and my localllll machine so you can check the webhook
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
    
    # print(session) # i can get the email and mark the session is booked 

    if session.mode == 'payment' and session.payment_status == 'paid':
      appointment_id = session.metadata['appointment_id']
      user_id = session.metadata['user_id']
      user = User.objects.get(id = user_id)

      appointment = Appointement.objects.get(id = appointment_id)  
      appointment.user= user
      appointment.state = 'booked'
      appointment.save()
      

      return HttpResponse(status=200)
    else :
      return HttpResponse(status=400)
  
  else:
      return HttpResponse(status=200)
      # print('Unhandled event type {}'.format(event['type']))
      # return HttpResponse(status=500)

