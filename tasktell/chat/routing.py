from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:pk>/', consumers.ChatConsumer.as_asgi()),
]