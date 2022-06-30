import jwt
from django.db.models import Q
from django.utils.crypto import get_random_string
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import User
from .models import Message, Room
from event_management import settings
from vendors.models import VendorRegistration


def create_room(sender, receiver):
    """
    :param sender: user id of the user that wants to send the message
    :param receiver: user id of the user to whom the message is to be sent
    :return: room
    """
    sender_user = User.objects.get(id=sender)
    receiver_user = User.objects.get(id=receiver)
    get_room = Room.objects.filter(Q(sender_user=sender_user, receiver_user=receiver_user) |
                                   Q(sender_user=receiver_user, receiver_user=sender_user))

    if get_room:
        room_name = get_room[0].room_name
        return room_name

    else:
        room_name = get_random_string(10)

        while True:
            room_exists = Room.objects.filter(room_name=room_name)
            if room_exists:
                room_name = get_random_string(10)
            else:
                break

        new_room = Room.objects.create(sender_user=sender_user, receiver_user=receiver_user, room_name=room_name)
        new_room.save()
        return new_room


class UserValidationView(View):
    """
    view to get user from token
    """

    def get(self, request):
        return render(request, template_name='chat/user_validation.html')

    def post(self, request):
        token = request.POST['token']
        try:
            valid_data = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            sender = valid_data['user_id']
            request.session.flush()
            request.session['user'] = sender
            request.session['token'] = token
            return redirect('rooms')

        except Exception as e:
            return render(request, 'chat/user_validation.html', {'error': e})


def rooms(request):
    sender = request.session['user']
    get_rooms = Room.objects.filter(Q(sender_user=sender) | Q(receiver_user=sender))
    return render(request, 'chat/choice.html', {'user': sender, 'rooms': get_rooms})


class GetEventManagers(View):
    """
    class to select an event manager to chat
    """
    def get(self, request):
        event_managers = User.objects.filter(is_event_manager=True)
        return render(request, 'chat/get_event_manager.html', {'event_managers': event_managers})

    def post(self, request):
        sender = request.session.get('user')
        receiver = request.POST['event_managers']
        request.session['receiver_user'] = receiver
        room_name = create_room(sender, receiver)
        return redirect('room', room_name=room_name)


class GetVendors(View):
    """
    class to select a vendor to chat
    """
    def get(self, request):
        vendors = VendorRegistration.objects.filter(is_approved=True)
        return render(request, 'chat/get_vendor.html', {'vendors': vendors})

    def post(self, request):
        sender = request.session.get('user')
        receiver = request.POST['vendors']
        request.session['receiver_user'] = receiver
        room_name = create_room(sender, receiver)
        return redirect('room', room_name=room_name)


class ChatRoom(View):
    queryset = Room.objects.all()

    def get(self, request, room_name, *args, **kwargs):
        get_object_or_404(Room, room_name=self.kwargs.get("room_name"))
        room = Room.objects.get(room_name=self.kwargs.get("room_name"))
        sender = request.session.get('user')
        sender_obj = User.objects.get(id=sender)
        sender_name = sender_obj.username

        if room.receiver_user.id == sender:
            receiver = room.sender_user.id
        else:
            receiver = room.receiver_user.id

        messages = Message.objects.filter(Q(sender_user=sender, receiver_user=receiver) |
                                         Q(sender_user=receiver, receiver_user=sender)).order_by('timestamp')

        return render(request, 'chat/room.html', {
            'room_name': room_name,
            'sender_id': sender,
            'receiver_id': receiver,
            'messages': messages,
            'sender_name': sender_name
        })



