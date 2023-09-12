from app.core.models import Chat
from app.core.types import ChatCompletionMessagesInput, ChatCompletionMessagesItem


async def build_messages_input(chat: Chat, message: str, context: str) -> ChatCompletionMessagesInput:
    messages_input: ChatCompletionMessagesInput = []
    messages_input.append(
        ChatCompletionMessagesItem(
            role="system",
            content=(
                f"You are a helpful assistant "
                f"Bellow there is some context you should use to answer the questions "
                f"The pieces of information are separated by:---\nCONTEXT->{context}."
            ),
        )
    )

    async for msg in chat.messages.filter(response_association__isnull=False).select_related(
        "response_association__response"
    ).order_by("created_at"):
        response_association = msg.response_association
        response = response_association.response
        messages_input.append(ChatCompletionMessagesItem(role="user", content=msg.content))
        messages_input.append(ChatCompletionMessagesItem(role="assistant", content=response.content))

    messages_input.append(ChatCompletionMessagesItem(role="user", content=message))

    return messages_input
