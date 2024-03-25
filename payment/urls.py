from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt
from .views import SessionView , CreateCheckoutSessionView , WebhookView , Successview  , Cancelview
from rest_framework.routers import DefaultRouter



router2 = DefaultRouter()
router2.register(r'Sessions', SessionView)


urlpatterns = [
       path('', include(router2.urls)),
       path('CheckoutSessions/<int:pk>/', CreateCheckoutSessionView.as_view()),
       path('WebhookView', WebhookView),
       path('Success',Successview.as_view()),
       path('Cancel',Cancelview.as_view())

]