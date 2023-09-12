import json
import openai
import dataclasses
from django.conf import settings
from app.core.models import Chat
from app.core.services.tokens import num_tokens_from_string_gpt_35

from app.core.types import ChatCompletionMessagesInput, ChatCompletionMessagesItem


TITLE_REQUEST_TEMPLATE = """
You are a chatbot that answers questions about a project, the messages are stored in a database
for future similar questions, given the question and your answer below what would you title the
chat with a maximum of 255 characters?
MESSAGE: {message}
---
YOUR ANSWER: {answer}
"""


async def get_response(messages_input: ChatCompletionMessagesInput) -> str:
    messages = [dataclasses.asdict(message) for message in messages_input]
    print(num_tokens_from_string_gpt_35(json.dumps(messages)))
    result = await openai.ChatCompletion.acreate(
        model=settings.DJOCS_GPT_MODEL,
        messages=[dataclasses.asdict(message) for message in messages_input],
        temperature=0.2,
    )
    return result["choices"][0]["message"]["content"]  # type: ignore


async def get_chat_title_from_message(message: str, answer: str) -> str:
    message = TITLE_REQUEST_TEMPLATE.format(message=message, answer=answer)
    messages_input = [
        ChatCompletionMessagesItem(role="system", content=TITLE_REQUEST_TEMPLATE),
        ChatCompletionMessagesItem(role="user", content=message),
    ]
    return await get_response(messages_input=messages_input)
