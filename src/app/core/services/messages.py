from app.core.models import Chat, Message, User

async def create_message(chat: Chat, author: User, content: str, embedding: list[float]) -> Message:
    message: Message = await Message.objects.acreate(chat=chat, author=author, content=content, embedding=embedding)
    return message







