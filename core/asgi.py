"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from django.urls.conf import include
from channels.sessions import SessionMiddlewareStack


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

from home import routers


ws_pattern = [
    path('ws/', routers.ws_pattern)
]

application = SessionMiddlewareStack(ProtocolTypeRouter({
    "websocket": URLRouter(ws_pattern)
}))
