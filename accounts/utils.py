from django.core.mail import EmailMessage 
import secrets 
from .models import User , otpcode 
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail

def send_generated_otp_to_email(email): 
    subject = "Sending OTP for Email verification"
    otp =secrets.token_hex(3)[:5]
    user = User.objects.get(email=email)
    message =f"Hi {user.name} , here is your otp code {otp} , it expires in 5 minutes "
    sender =settings.EMAIL_HOST_USER
    try:
        otp_obj = otpcode.objects.get(user=user)
        # Update the existing OTP object
        otp_obj.otp = otp
        otp_obj.otp_expires_at = timezone.now() + timezone.timedelta(minutes=5)
    except otpcode.DoesNotExist:
         # Create a new OTP object
        otp_obj = otpcode.objects.create(user=user, otp=otp)
        otp_obj.otp_expires_at = timezone.now() + timezone.timedelta(minutes=5)
        
    otp_obj.save()

   
    # email credentials
    receiver = [email, ]
          # send email
    send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )
  
