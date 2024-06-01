from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status, generics
from reservations.models import Appointement 
from django.conf import settings
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import redirect
import stripe
from accounts.models import Patient , User
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated



stripe.api_key = settings.STRIPE_SECRET_KEY

Local='http://127.0.0.1:8000/'
PublicDomain='https://sightsaver.onrender.com/'

class SuccessView(APIView):
    def get(self, request):
        return Response({"message": "Thanks for dealing with us, check your notifications."})

class CancelView(APIView):
    def get(self, request):
        return Response({"message": "Payment is canceled"})

class CreateCheckoutSessionView(APIView):
    def get(self, request):
        appointment_id = request.GET.get('appointment_id')
        user_id = request.GET.get('user_id')

        if not appointment_id or not user_id:
            return Response({'message': 'appointment_id and user_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            appointment_id = int(appointment_id)
            user_id = int(user_id)
        except ValueError:
            return Response({'message': 'Invalid appointment_id or user_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            appointment_instance = Appointement.objects.get(id=appointment_id)
        except Appointement.DoesNotExist:
            return Response({'message': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            checkout_stripe_session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'egp',
                        'unit_amount': int(appointment_instance.price) * 100,
                        'product_data': {
                            'name': f"{appointment_instance.type} session"
                        }
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=PublicDomain + 'payment/success',
                cancel_url=PublicDomain + 'payment/cancel',
                metadata={'user_id': user_id, 'appointment_id': appointment_id}
            )
            return Response({"url":checkout_stripe_session.url},status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'message': 'Error creating Stripe session', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    if sig_header is None:
        return HttpResponse(status=400)
    
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_KEY)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        if session.mode == 'payment' and session.payment_status == 'paid':
            appointment_id = session.metadata['appointment_id']
            user_id = session.metadata['user_id']
            
            try:
                user = User.objects.get(id=user_id)
                appointment = Appointement.objects.get(id=appointment_id)
                appointment.user = user
                appointment.state = 'booked'
                appointment.save()

                # Create notifications
                patient_message = f"You booked an appointment at {appointment.start_at} with Dr. {appointment.doctor.user.name} successfully"
                doctor_message = f"{user.name} has booked an appointment at {appointment.start_at} with you"

                Notification.objects.create(user=user, message=patient_message)
                Notification.objects.create(user=appointment.doctor.user, message=doctor_message)

            except (User.DoesNotExist, Appointement.DoesNotExist):
                return HttpResponse(status=400)
            return HttpResponse(status=200)
    return HttpResponse(status=200)


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
      
      
# Return a JSON response with a key "unread_notifications_exist" which will be true if there are unread notifications and false otherwise
class UnreadNotificationCheck(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        unread_notifications_exist = Notification.objects.filter(user=request.user, is_read=False).exists()
        return Response({"unread_notifications_exist": unread_notifications_exist}, status=status.HTTP_200_OK)