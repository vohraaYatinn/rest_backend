# routing.py in orders app

from django.urls import path
from django.urls import re_path

from .consumer import OrderConsumer

websocket_urlpatterns = [
    re_path(r'ws/orders/', OrderConsumer.as_asgi()),  # Update with your consumer
]
