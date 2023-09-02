from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from app.core.services.llms.openai import get_chat_title_from_message, get_message_response
from .models import Chat, Message, MessageResponse
from asgiref.sync import sync_to_async


async def index(request: HttpRequest) -> HttpResponse:
    chats = []
    qs = Chat.objects.filter(active=True, title__isnull=False).exclude(title="").order_by("-created_at")
    async for chat in qs.select_related("author", "author__profile"):
        chats.append(chat)
    return render(request, "index.html", {"chats": chats})


async def list_chats(request: HttpRequest) -> HttpResponse:
    chats = []
    qs = Chat.objects.filter(active=True, title__isnull=False).exclude(title="").order_by("-created_at")
    async for chat in qs.select_related("author", "author__profile"):
        chats.append(chat)
    if request.htmx:  # type: ignore
        return render(request, "chat_history/chat_history_partial.html", {"chats": chats})
    return render(request, "chat_history/chat_history_page.html", {"chats": chats})


async def get_chat(request: HttpRequest, chat_id: str) -> HttpResponse:
    chat: Chat = await sync_to_async(get_object_or_404)(Chat, id=chat_id, active=True)
    messages = []
    async for message in Message.objects.filter(chat=chat, active=True).order_by("created_at").select_related("author"):
        messages.append(message)
    if request.htmx:  # type: ignore
        return render(request, "chat/chat_partial.html", {"chat": chat, "messages": messages})
    return render(request, "chat/chat_page.html", {"chat": chat, "messages": messages})


async def send_message(request: HttpRequest, chat_id: str) -> HttpResponse:
    chat: Chat = await sync_to_async(get_object_or_404)(Chat, id=chat_id, active=True)
    if request.method == "POST":
        content: str | None = request.POST.get("content")
        if content:
            message: Message = await Message.objects.acreate(chat=chat, author=request.user, content=content)
            llm_response = await get_message_response(content)
            if not chat.title:
                chat.title = await get_chat_title_from_message(message.content, llm_response)
                await chat.asave()

            response = await Message.objects.acreate(
                chat=chat,
                author=request.user,
                content=llm_response,
                type=Message.Type.LLM_RESPONSE,
            )
            message_response = await MessageResponse.objects.acreate(message=message, response=response)
            messages = []
            async for message in Message.objects.filter(chat=chat, active=True).order_by("created_at").select_related(
                "author"
            ):
                messages.append(message)
            return render(
                request,
                "chat/chat_partial.html",
                {"chat": chat, "messages": messages, "message_response": message_response},
            )
        return render(request, "error.html", {"error": "Missing content"})

    return render(request, "chat/send_message.html", {"chat": chat})


async def create_chat(request: HttpRequest) -> HttpResponse:
    chat: Chat = await Chat.objects.acreate(author=request.user)
    return HttpResponseRedirect(f"/chat/{chat.id}/")


async def list_messages(request: HttpRequest, chat_id: str) -> HttpResponse:
    messages = []
    async for message in Message.objects.filter(chat__id=chat_id, active=True).order_by("created_at").select_related(
        "author"
    ):
        messages.append(message)

    return render(request, "chat/chat_messages_list.html", {"messages": messages})
