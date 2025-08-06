import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import writers_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'professional_writers.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            writers_app.routing.websocket_urlpatterns
        )
    ),
})