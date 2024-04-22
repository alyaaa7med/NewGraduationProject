from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt
from .views import CreateCheckoutSessionView , WebhookView , Successview  , Cancelview





urlpatterns = [
       path('checkout-session', CreateCheckoutSessionView.as_view()),
       path('WebhookView', WebhookView),
       path('success',Successview.as_view()), #/<int:id>
       path('cancel',Cancelview.as_view())

]