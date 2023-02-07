import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import tasktell.chat.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tasktell.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            tasktell.chat.routing.websocket_urlpatterns
        )
    ),
})
