from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt
from .views import CreateCheckoutSessionView , WebhookView , SuccessView  , CancelView , NotificationListView , UnreadNotificationCheck





urlpatterns = [
       path('checkout-session', CreateCheckoutSessionView.as_view()),
       path('WebhookView', WebhookView),
       path('success',SuccessView.as_view()), #/<int:id>
       path('cancel',CancelView.as_view()),
       path('notifications/', NotificationListView.as_view(), name='notifications'),
       path('notifications/unread-check/', UnreadNotificationCheck.as_view(), name='unread-notification-check'),

]