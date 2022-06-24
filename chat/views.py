import jwt
from django.db.models import Q
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer

from accounts.models import User
from .models import Message
from event_management import settings
from vendors.models import VendorRegistration


def create_room(sender, receiver):
    """

    :param sender: user id of the user that sends the message
    :param receiver: user id of the user to whom the message is to be sent
    :return: room
    """
    sender_user = User.objects.get(id=sender)
    receiver_user = User.objects.get(id=receiver)
    room_name = f"{sender}_and_{receiver}"
    room = f"{receiver}_and_{sender}"
    all_rooms = Message.objects.filter(Q(room_name=room_name) | Q(room_name=room))

    if all_rooms:
        return HttpResponse("Room exists")
    else:
        create_room = Message.objects.create(sender_user=sender_user, receiver_user=receiver_user,
                                             room_name=room_name)
        create_room.save()
        return HttpResponse(room_name)


class UserValidationView(View):
    """
    view to get user from token
    """

    def get(self, request):
        return render(request, template_name='chat/user_validation.html')

    def post(self, request):
        token = request.POST['token']
        valid_data = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        user = valid_data['user_id']
        del request.session['user']
        request.session.modified = True
        request.session['user'] = user
        return render(request, 'chat/choice.html', {'user': user})


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
        return create_room(sender, receiver)


class GetVendors(View):
    """
    class to select a vendor to chat
    """
    def get(self, request):
        vendors = VendorRegistration.objects.filter(is_approved=True)
        return render(request, 'chat/get_vendor.html', {'vendors': vendors})

    def post(self, request):
        sender = int(request.session.get('user'))
        receiver = int(request.POST['vendors'])
        return create_room(sender, receiver)
