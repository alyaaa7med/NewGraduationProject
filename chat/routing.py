from channels.routing import ProtocolTypeRouter, URLRouter
# import app.routing
from django.urls import re_path
from .consumers import TextRoomConsumer

from django.urls import path


# Here, "" is routing to the URL PersonalChatConsumer which
# will handle the chat functionality.

websocket_urlpatterns = [
	path('ws/<room_name>/' , TextRoomConsumer.as_asgi()) ,
]
