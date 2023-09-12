from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("chat/list/", views.list_chats, name="list-chats"),
    path("chat/create/", views.create_chat, name="create-chat"),
    path("chat/<str:chat_id>/", views.get_chat, name="get-chat"),
    path("chat/<str:chat_id>/send_message/", views.send_message, name="send-message"),
    path("chat/<str:chat_id>/messages/", views.list_messages, name="list-messages"),
    path("chat/<str:chat_id>/template-messages/", views.list_template_messages, name="list-template-messages"),
]
