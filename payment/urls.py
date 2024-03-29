from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt
from .views import CreateCheckoutSessionView , WebhookView , Successview  , Cancelview





urlpatterns = [
       path('CheckoutSessions/<int:pk>/', CreateCheckoutSessionView.as_view()),
       path('WebhookView', WebhookView),
       path('Success',Successview.as_view()),
       path('Cancel',Cancelview.as_view())

]