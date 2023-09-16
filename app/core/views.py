from django.shortcuts import render, get_object_or_404
from app.core.services.context import get_context_from_knowledges
from app.core.services import messages as messages_service
from app.core.services import knowledges as knowledges_service
from app.core.services import chat as chat_service
from app.core.services import embeddings as embeddings_service
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from app.core.services.llm import get_chat_title_from_message, get_response
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

    if request.method == "GET":
        return render(request, "chat/send_message.html", {"chat": chat})
    elif request.method == "POST":
        content: str | None = request.POST.get("content")
        if not content:
            return render(request, "error.html", {"error": "Missing content"})

        message = await messages_service.create_message(chat=chat, author=request.user, content=content)
        message_embedding = await embeddings_service.get_content_embedding(content)

        knowledges = await knowledges_service.get_relevant_knowledges_for_message_embedding(message_embedding)

        context = await get_context_from_knowledges(knowledges)
        # context + history cant be more than 1000 characters?

        messages_input = await chat_service.build_messages_input(chat, content, context)
        llm_response = await get_response(messages_input=messages_input)
        if not chat.title:
            chat.title = await get_chat_title_from_message(message.content, llm_response)
            await chat.asave()

        response = await Message.objects.acreate(
            chat=chat,
            author=request.user,
            content=llm_response,
            type=Message.Type.LLM_RESPONSE,
        )
        await MessageResponse.objects.acreate(message=message, response=response)
        messages = []
        async for message in Message.objects.filter(chat=chat, active=True).order_by("created_at").select_related(
            "author"
        ):
            messages.append(message)
        return render(
            request,
            "chat/chat_page.html",
            {"chat": chat, "messages": messages, "message": message, "response": response},
        )
    else:
        return render(request, "error.html", {"error": "Method not allowed"}, status=405)


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

async def list_template_messages(request: HttpRequest, chat_id: str) -> HttpResponse:
    messages = []
    async for message in Message.objects.filter(chat__id=chat_id, active=True, type=Message.Type.MODERATOR_MESSAGE).order_by("created_at").select_related(
        "author"
    ):
        messages.append(message)

    return render(request, "chat_history/chat_history_template_message_list.html", {"messages": messages})
