# chat/routing.py

from django.urls import re_path

from . import consumers

#Making Websocket routing URL
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_id>\d+)/messages$', consumers.ChatConsumer.as_asgi()),
]


#daphne backend.asgi:application