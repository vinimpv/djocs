from dataclasses import dataclass
from typing import Literal

@dataclass
class ChatCompletionMessagesItem:
    role: Literal["system", "user", "assistant"]
    content: str

ChatCompletionMessagesInput = list[ChatCompletionMessagesItem]
