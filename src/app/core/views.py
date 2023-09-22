from django.shortcuts import redirect, render, get_object_or_404
from app.core.services.context import get_context_from_knowledges
from app.core.services import messages as messages_service
from app.core.services import knowledges as knowledges_service
from app.core.services import chat as chat_service
from app.core.services import embeddings as embeddings_service
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from app.core.services.llm import get_chat_title_from_message, get_response
from .models import Chat, Message, MessageResponse
from asgiref.sync import sync_to_async
from typing import Callable, Coroutine, ParamSpec, cast
from django.contrib.auth.models import User

P = ParamSpec("P")

def get_user(request: HttpRequest) -> User | None:
    return cast(User, request.user) if request.user.is_authenticated else None


def require_auth(
    fn: Callable[P, Coroutine[None, None, HttpResponse]]
) -> Callable[[HttpRequest], Coroutine[None, None, HttpResponse]]:
    async def wrapper(request: HttpRequest, *args: P.args, **kwargs: P.kwargs) -> HttpResponse:
        kwargs["request"] = request
        user = await sync_to_async(get_user)(request)
        if not user:
            return redirect("/accounts/login/")
        kwargs["user"] = user
        return await fn(*args, **kwargs)

    return wrapper


@require_auth
async def index(request: HttpRequest, user: User) -> HttpResponse:
    chats = []
    qs = Chat.objects.filter(author=user, active=True, title__isnull=False).exclude(title="").order_by("-created_at")
    async for chat in qs.select_related("author", "author__profile"):
        chats.append(chat)
    return render(request, "index.html", {"chats": chats})


@require_auth
async def list_chats(request: HttpRequest, user: User) -> HttpResponse:
    chats = []
    qs = Chat.objects.filter(author=user, active=True, title__isnull=False).exclude(title="").order_by("-created_at")
    async for chat in qs.select_related("author", "author__profile"):
        chats.append(chat)
    if request.htmx:  # type: ignore
        return render(request, "chat_history/chat_history_partial.html", {"chats": chats})
    return render(request, "chat_history/chat_history_page.html", {"chats": chats})


@require_auth
async def get_chat(request: HttpRequest, chat_id: str, user) -> HttpResponse:
    chat: Chat = await sync_to_async(get_object_or_404)(Chat, id=chat_id, active=True, author=user)
    messages = []
    async for message in Message.objects.filter(chat=chat, active=True, author=user).order_by(
        "created_at"
    ).select_related("author"):
        messages.append(message)
    if request.htmx:  # type: ignore
        return render(request, "chat/chat_partial.html", {"chat": chat, "messages": messages})
    return render(request, "chat/chat_page.html", {"chat": chat, "messages": messages})


@require_auth
async def send_message(request: HttpRequest,user: User, chat_id: str) -> HttpResponse:
    chat: Chat = await sync_to_async(get_object_or_404)(Chat, id=chat_id, active=True, author=user)

    if request.method == "GET":
        return render(request, "chat/send_message.html", {"chat": chat})
    elif request.method == "POST":
        content: str | None = request.POST.get("content")
        if not content:
            return render(request, "error.html", {"error": "Missing content"})

        message = await messages_service.create_message(chat=chat, author=user, content=content)
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


@require_auth
async def create_chat(request: HttpRequest, user: User) -> HttpResponse:
    chat: Chat = await Chat.objects.acreate(author=user)
    return HttpResponseRedirect(f"/chat/{chat.id}/")


@require_auth
async def list_messages(request: HttpRequest, user: User, chat_id: str) -> HttpResponse:
    chat = await sync_to_async(get_object_or_404)(Chat, id=chat_id, active=True, author=user)
    if not chat:
        return render(request, "error.html", {"error": "Chat not found"}, status=404)

    messages = []
    async for message in Message.objects.filter(chat__id=chat.id, active=True).order_by("created_at").select_related(
        "author"
    ):
        messages.append(message)

    return render(request, "chat/chat_messages_list.html", {"messages": messages})


@require_auth
async def list_template_messages(request: HttpRequest, chat_id: str) -> HttpResponse:
    messages = []
    async for message in Message.objects.filter(
        chat__id=chat_id, active=True, type=Message.Type.MODERATOR_MESSAGE
    ).order_by("created_at").select_related("author"):
        messages.append(message)

    return render(request, "chat_history/chat_history_template_message_list.html", {"messages": messages})
