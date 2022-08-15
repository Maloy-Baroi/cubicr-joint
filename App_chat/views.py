from django.contrib.auth.models import Group
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render


# Create your views here.
from App_auth.models import CustomUser
from App_chat.models import MessageModel, Room


def myChatRooms(request):
    messages = MessageModel.objects.filter(user=request.user)
    groups = request.user.groups.all()
    content = {
        'message': messages,
        'groups': groups,
        'groupsCount': groups.count(),
    }
    return render(request, 'App_chat/AllChats.html', context=content)


def getMessages(request, room):
    roomDetails = Room.objects.get(name=room)
    messages = MessageModel.objects.filter(room=roomDetails.id)
    listMessages = []
    for i in messages.values():
        user = CustomUser.objects.get(id=i['user_id'])
        i['userID'] = user.id
        i['username'] = user.user_main_profile.fullName
        i['profile_picture'] = user.user_main_profile.profile_picture.url
        x_date = str(i['date'])[:16]
        i['date'] = x_date
        listMessages.append(i)
    return JsonResponse({"messagesList": listMessages})


def messageSend(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        room = request.POST.get('room_name')
        userID = request.POST.get('user_id')
        user = CustomUser.objects.get(id=userID)
        thisRoom = Room.objects.get(name=room)
        newMessage = MessageModel.objects.create(value=message, user=user, room=thisRoom)
        newMessage.save()
        return HttpResponse("Message Send Successfully")

