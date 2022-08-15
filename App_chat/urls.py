from django.urls import path
from App_chat.views import *

app_name = 'App_chat'


urlpatterns = [
    path('my-chat-groups/', myChatRooms, name='my-chat-groups'),
    # path('chatRoom/<str:roomNumber>/', chatRoom, name='chatRoom'),
    # path('checkRoomView/', checkRoomView, name='checkRoomView'),
    path('getMessages/<str:room>/', getMessages, name='getMessages'),
    path('send-message/', messageSend, name='message-send'),
    # path('register/', account_creation_view, name='register'),
    # path('login/', login_view, name='login'),
]
