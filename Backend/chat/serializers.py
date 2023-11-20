from rest_framework import serializers
from .models import Chat, Message
from authen.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    
    """
    Serializer for the Message model.

    This serializer is used to convert Message model instances to JSON and vice versa.
    """
    
    sender = UserSerializer()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']

class ChatSerializer(serializers.ModelSerializer):
    
    """
    Serializer for the Chat model.

    This serializer is used to convert Chat model instances to JSON and vice versa.
    """
    
    
    users = UserSerializer(many=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'users', 'messages']