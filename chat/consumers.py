import json

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from django.contrib.auth.models import User

from .models import Message, Room


class JoinAndLeave(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        message_type = text_data.get("type", None)
        if message_type:
            data = text_data.get("data", None)
        if message_type == "leave_room":
            self.leave_room(data)
        elif message_type == "join_room":
            self.join_room(data)

    def leave_room(self, room_uuid):
        room = Room.objects.get(uuid=room_uuid)
        room.remove_user_from_room(self.user)
        data = {
            "type": "leave_room",
            "data": room_uuid
        }
        self.send(json.dumps(data))

    def join_room(self, room_uuid):
        room = Room.objects.get(uuid=room_uuid)
        room.add_user_to_room(self.user)
        data = {
            "type": "join_room",
            "data": room_uuid
        }
        self.send(json.dumps(data))



class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_uuid = str(self.scope["url_route"]["kwargs"]["uuid"])
        self.room = await database_sync_to_async(Room.objects.get)(uuid=self.room_uuid)
        await self.channel_layer.group_add(
            self.room_uuid, self.channel_name)
        self.user = self.scope["user"]
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        message_type = text_data.get("type", None)
        message = text_data.get("message", None)
        author = text_data.get("author", None)
        if message_type == "text_message":
            user = await database_sync_to_async(User.objects.get)(username=author)
            _message = await database_sync_to_async(Message.objects.create)(
                author=user,
                content=message,
                room=self.room
            )

        await self.channel_layer.group_send(self.room_uuid, {
            "type": "text_message",
            "message": str(message),
            "author_name": "{} {}".format(user.first_name, user.last_name),
            "author_email": user.email,
        })

    async def text_message(self, event):
        message = event["message"]
        author_email = event.get("author_email")
        author_name = event.get("author_name")

        returned_data = {
            "type": "text_message",
            "message": message,
            "room_uuid": self.room_uuid,
            "author_email": author_email,
            "author_name": author_name,
        }
        await self.send(json.dumps(
            returned_data
        ))

    async def event_message(self, event):
        message = event.get("message")
        user = event.get("user", None)

        await self.send(
            json.dumps(
                {
                    "type": "event_message",
                    "message": message,
                    "status": event.get("status", None),
                    "user": user
                }
            )
        )
