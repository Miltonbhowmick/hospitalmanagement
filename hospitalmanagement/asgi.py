import os
from .wsgi import * 
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import hospitalmanagement.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hospitalmanagement.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            hospitalmanagement.routing.websocket_urlpatterns
        )
    ),
})