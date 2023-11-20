
# from djongo import models
from django.db import models
from authen.models import User

class Chat(models.Model):
    """
    This model is representing a chat.

    A chat consists of multiple(two) users and messages.
    """
    
    #Tried the mongo ArrayReferenceField but failed and used db.models ManytoManyField
    # users = models.ArrayReferenceField(
    #     to=User,
    #     on_delete=models.CASCADE,
    #     related_name='chats'
    # )
    users = models.ManyToManyField(User, related_name='chats')

class Message(models.Model):
    
    """
    This model is representing a message in a chat.

    Each message is associated with a specific chat, sender, and timestamp.
    """
    
    """
    Foreign Key relationship field linking the Message model to the Chat model.

    This field represents the chat to which the message belongs.
    """
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    
    """
    Foreign Key relationship field linking the Message model to the User model.

    This field represents the user who sent the message.
    """
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    
    """
    Text field representing the content of the message.
    """
    content = models.TextField()
    
    """
    DateTime field representing the timestamp when the message was created.
    
    This field is automatically set to the current date and time when a new message is created.
    """
    timestamp = models.DateTimeField(auto_now_add=True)