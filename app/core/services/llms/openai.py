import openai

TITLE_REQUEST_TEMPLATE = """
You are a chatbot that answers questions about a project, the messages are stored in a database
for future similar questions, given the question and your answer below what would you title the chat with a maximum of 255 characters?
MESSAGE: {message}
---
YOUR ANSWER: {answer}
"""

EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"


async def get_chat_title_from_message(message: str, answer: str) -> str:
    result = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a world class software engineer that answers questions about a project.",
            },
            {"role": "user", "content": TITLE_REQUEST_TEMPLATE.format(message=message, answer=answer)},
        ],
    )
    return result["choices"][0]["message"]["content"] # type: ignore


async def get_message_response(message: str) -> str:
    result = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a world class software engineer."},
            {"role": "user", "content": message},
        ],
    )
    return result["choices"][0]["message"]["content"] # type: ignore

