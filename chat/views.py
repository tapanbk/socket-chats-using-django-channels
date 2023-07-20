# chat/views.py
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from .models import Room
from django.contrib.auth.decorators import login_required


@login_required
def home_view(request):
    """
        The homepage where all rooms are listed
    """
    rooms = Room.objects.all()
    user = request.user
    context = {
        "rooms": rooms,
        "user": user
    }
    return render(request, template_name="chat/home.html", context=context)


@login_required
def rooms_view(request):
    """
        The view for a room where all messages and events are sent to the frontend
    """
    rooms = Room.objects.all()
    context = {
        "message_and_event_list": [],
        "room_members": [],
        "rooms": rooms,
    }
    return render(request, template_name="chat/room_chat.html", context=context)


@login_required
def room_chat_view(request, uuid):
    """
        The view for a room where all messages and events are sent to the frontend
    """

    room = get_object_or_404(Room, uuid=uuid)
    if request.user not in room.members.all():
        return HttpResponseForbidden("You are not a member of this room. Kindly use the join button")

    messages = room.message_set.all()
    """
        messages are the message the members of a room send to the room
    """

    events = room.event_set.all()
    """
        events are the messages that indicates that a user joined or left the room.
        They will be sent automatically when a user join or leave the room
    """

    # Combine the events and messages for a room
    message_and_event_list = [*messages, *events]

    # Sort the combination by the timestamp so that they are listed in order
    sorted_message_event_list = sorted(message_and_event_list, key=lambda x: x.timestamp)

    # get the list of all room members
    room_members = room.members.all()
    rooms = Room.objects.filter(members=request.user).all()
    context = {
        "message_and_event_list": sorted_message_event_list,
        "room_members": room_members,
        "rooms": rooms,
        'current_room': room
    }
    return render(request, template_name="chat/room_chat.html", context=context)
