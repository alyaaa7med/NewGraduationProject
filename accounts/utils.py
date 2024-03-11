from django.core.mail import EmailMessage 
import secrets 
from .models import User , otpcode 
from django.conf import settings
from django.utils import timezone


def send_generated_otp_to_email(email): 
    subject = "OTP for Email verification"
    otp = otp=secrets.token_hex(3)[:5]
    # user = User.objects.get(email=email)
    email_body=f"Hi , here is your otp code {otp} , it expires in 5 minutes "
    from_email=settings.EMAIL_HOST
    # try:
    #     otp_obj = otpcode.objects.get(user=user)
    #     # Update the existing OTP object
    #     otp_obj.otp = otp
    #     otp_obj.otp_expires_at = timezone.now() + timezone.timedelta(minutes=5)
    # except otpcode.DoesNotExist:
    #      # Create a new OTP object
    #     otp_obj = otpcode.objects.create(user=user, otp=otp)
    #     otp_obj.otp_expires_at = timezone.now() + timezone.timedelta(minutes=5)
        
    # otp_obj.save()

    #send the email 
    d_email=EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[email])
    d_email.send()

