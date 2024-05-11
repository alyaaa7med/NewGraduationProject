"""
ASGI config for django_ project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from chat.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sightsaver.settings')

application = get_asgi_application()


# the websocket will open at 127.0.0.1:8000/ws/<room_name>/
# application = ProtocolTypeRouter({
    
#     "http" : application,
#     'websocket':
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ,
# })
