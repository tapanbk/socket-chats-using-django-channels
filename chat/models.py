from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4

from django.urls import reverse

User = get_user_model()


class Room(models.Model):
    """
    The room model where multiple users can share and discuss ideas
    """
    uuid = models.UUIDField(default=uuid4, editable=False)
    name = models.CharField(max_length=30)
    members = models.ManyToManyField(User)

    def __str__(self) -> str:
        return f"Room {self.name}-{self.uuid}"

    def get_absolute_url(self):
        return reverse("room", args=[str(self.uuid)])

    def add_user_to_room(self, user: User):
        """
            A helper function to add a user to a room and create an event object
        """
        self.members.add(user)
        self.event_set.create(type="Join", user=user)
        self.save()

    def remove_user_from_room(self, user: User):
        """
            A helper function to remove users from room members when they
            leave the room and create an event for the timestamp the user left the room
        """
        self.members.remove(user)
        self.event_set.create(type="Left", user=user)
        self.save()

    def is_in_room(self, user: User) -> bool:
        """
            A helper function to remove users from room members when they
            leave the room and create an event for the timestamp the user left the room
        """
        return user in self.members.all()


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self) -> str:
        date = self.timestamp.date()
        time = self.timestamp.time()
        return f"{self.author}:- {self.content} @{date} {time.hour}:{time.minute}"


class Event(models.Model):
    """
    A model that holds all events related to a room like when a user joins the room or leaves.
    """
    CHOICES = [
        ("Join", "join"),
        ("Left", "left")
    ]
    type = models.CharField(choices=CHOICES, max_length=50)
    description = models.CharField(help_text="A description of the event that occurred", max_length=300, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.description = f"{self.user} {self.type} the {self.room.name} room"
        super().save(*args, kwargs)

    def __str__(self) -> str:
        return f"{self.description}"
