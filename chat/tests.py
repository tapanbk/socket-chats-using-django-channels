from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Room, Message, Event

User = get_user_model()


class RoomModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.room = Room.objects.create(name='Test Room')
        self.room.members.add(self.user1)

    def test_room_str(self):
        self.assertEqual(str(self.room), f"Room {self.room.name}-{self.room.uuid}")

    def test_get_absolute_url(self):
        url = reverse('room', args=[str(self.room.uuid)])
        self.assertEqual(self.room.get_absolute_url(), url)

    def test_add_user_to_room(self):
        new_user = User.objects.create_user(username='newuser', password='newpassword')
        self.room.add_user_to_room(new_user)
        self.assertIn(new_user, self.room.members.all())

    def test_remove_user_from_room(self):
        self.room.remove_user_from_room(self.user1)
        self.assertNotIn(self.user1, self.room.members.all())

    def test_is_in_room(self):
        self.assertTrue(self.room.is_in_room(self.user1))
        self.assertFalse(self.room.is_in_room(self.user2))


class MessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.room = Room.objects.create(name='Test Room')
        self.message = Message.objects.create(author=self.user, content='Test message', room=self.room)

    def test_message_str(self):
        expected_str = f"{self.user}:- {self.message.content} @{self.message.timestamp.date()} {self.message.timestamp.time().hour}:{self.message.timestamp.time().minute}"
        self.assertEqual(str(self.message), expected_str)

    def test_message_author(self):
        self.assertEqual(self.message.author, self.user)

    def test_message_room(self):
        self.assertEqual(self.message.room, self.room)


class EventModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.room = Room.objects.create(name='Test Room')
        self.event = Event.objects.create(type='Join', user=self.user, room=self.room)

    def test_event_user(self):
        self.assertEqual(self.event.user, self.user)

    def test_event_room(self):
        self.assertEqual(self.event.room, self.room)
