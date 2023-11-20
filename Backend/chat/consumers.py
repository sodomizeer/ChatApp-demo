import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    
    """
    WebSocket consumer for handling chat interactions.

    This consumer handles WebSocket connections, disconnections, and message reception.
    """
    
    async def connect(self):
        
        """
        Called when the WebSocket is handshaking as part of the connection process.
        """
        
        await self.accept()

    async def disconnect(self, close_code):
        
        """
        Called when the WebSocket closes for any reason.
        """
        
        pass

    async def receive(self, text_data):
        
        """
        Called when the server receives a message from the WebSocket.

        param text_data: The received message data.
        type text_data: str
        """
        
        print(f"\n\nMessageDATA :{json.loads(text_data)}\n\n")
        try:
            message_data = json.loads(text_data)
            message = message_data["content"]  # Use get() to get the content, provide a default value if not present
            print(f"\n\nMessage content :{message['content']}\n\n")
            # Sending the message to other WebSocket consumers in the same group
            await self.send(text_data=json.dumps({
                'message': message['content']
            }))
        except json.JSONDecodeError:
            print("Failed to decode JSON:", text_data)