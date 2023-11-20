from django.shortcuts import render


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from authen.models import User 

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_chats(request):
    
    """
    View to retrieve all chats for the authenticated user.

    param request:      The HTTP request.
    type request:       rest_framework.request.Request
    return: HTTP        response containing chat data or an error message.
    return type:        rest_framework.response.Response
    """
    
    user = request.user
    chats = user.chats.all()
    serializer = ChatSerializer(chats, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_messages(request, chat_id):
    """
    View to retrieve all messages for a specific chat Room.

    param request:      The HTTP request.
    type request:       rest_framework.request.Request
    param chat_id:      The ID of the chat.
    type chat_id:       int
    return:             HTTP response containing message data or an error message.
    return type:        rest_framework.response.Response
    """
    user = request.user
    try:
        chat = user.chats.get(pk=chat_id)
        messages = chat.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    except Chat.DoesNotExist:
        return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_chat(request, chat_id):
    """
    View to delete a chat.

    param request:      The HTTP request.
    type request:       rest_framework.request.Request
    param chat_id:      The ID of the chatRoomw to be deleted.
    type chat_id:       int
    return:             HTTP response indicating success or failure.
    return type:        rest_framework.response.Response
    
    """
    user = request.user
    try:
        chat = user.chats.get(pk=chat_id)
        chat.delete()
        return Response({"message": "Chat deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Chat.DoesNotExist:
        return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)
    
    


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_chat(request):
    
    """
    View to create a new chat.

    param request:      The HTTP request.
    type request:       rest_framework.request.Request
    return:             HTTP response containing the created chat data or an error message.
    return type:        rest_framework.response.Response
    """
    
    user = request.user
    data = request.data

    user_emails = data.get("users", [])

    # Validates that there are exactly two users
    if len(user_emails) != 2:
        return Response({"error": "A chat must have exactly two users"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        chat = Chat.objects.create()
        
        users = User.objects.filter(email__in=user_emails)

        chat.users.set(users)

        serializer = ChatSerializer(chat)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_message(request, chat_id):
    
    """
    View to send a message to a chat.

    param request:      The HTTP request.
    type request:       rest_framework.request.Request
    param chat_id:      The ID of the chat.
    type chat_id:       int
    return:             HTTP response containing the created message data or an error message.
    return type:        rest_framework.response.Response
    """
    
    user = request.user
    data = request.data

    try:
        # Getting the chat
        chat = user.chats.get(pk=chat_id)

        # Createing a new message
        message = Message.objects.create(
            chat=chat,
            sender=user,
            content=data.get("content", "")
        )

        serializer = MessageSerializer(message)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Chat.DoesNotExist:
        return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request):
    """
    View to retrieve information about all users.

    param request:      The HTTP request. not used though!
    type request:       rest_framework.request.Request
    return:             HTTP response containing user data.
    return type:        rest_framework.response.Response
    """
    all_users  = User.objects.all()
    print(f"all users: {all_users}")
    user_data = [
        {
            'email':user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        for user in all_users
    ]

    return Response(user_data)