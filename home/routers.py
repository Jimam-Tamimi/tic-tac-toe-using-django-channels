from django.urls import path
from channels.routing import URLRouter

from .consumers import *



ws_pattern = URLRouter([
    path('play/<str:code>/<str:username>/',  GameConsumer.as_asgi())
])
