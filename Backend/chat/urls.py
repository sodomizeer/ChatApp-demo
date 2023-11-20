from django.urls import path
from .views import get_chats, get_messages, delete_chat, create_chat,send_message, get_user

urlpatterns = [
    path('chats/', get_chats, name='get_chats'),
    path('chats/<int:chat_id>/messages/', get_messages, name='get_messages'),
    path('chats/<int:chat_id>/', delete_chat, name='delete_chat'),
    path('create-chat/', create_chat, name='create_chat'),
    path('chats/<int:chat_id>/send-message/', send_message, name='send_message'),
    path("get_users/", get_user,name='get_users')
]