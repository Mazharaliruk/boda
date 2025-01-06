# mysite/asgi.py
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boda.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

from account.authmiddleware import JWTAuthMiddleware
from inventry.routing import category_url_patterns
from core.routing import cor_url_patterns

# Combine all WebSocket URL patterns
websocket_urlpatterns = [
    *category_url_patterns,
    *cor_url_patterns,
]

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": JWTAuthMiddleware(  # Wrap the WebSocket routes with your middleware
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
    }
)