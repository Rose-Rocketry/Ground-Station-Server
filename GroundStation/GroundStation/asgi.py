"""
ASGI config for GroundStation project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
import time

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GroundStation.settings')

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

import LaunchDataTracker.routing

application = ProtocolTypeRouter({
    'http':django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            LaunchDataTracker.routing.websocket_urlpatterns
        )
    )
    })
