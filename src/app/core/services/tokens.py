import tiktoken

def num_tokens_from_string(string: str, encoding: tiktoken.Encoding) -> int:
    """Returns the number of tokens in a text string."""
    num_tokens = len(encoding.encode(string))
    return num_tokens


def num_tokens_from_string_gpt_35(string: str) -> int:
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return num_tokens_from_string(string, encoding)


def num_tokens_from_string_gpt_4(string: str) -> int:
    encoding = tiktoken.encoding_for_model("gpt-4")
    return num_tokens_from_string(string, encoding)


def num_tokens_from_string_ada_2(string: str) -> int:
    encoding = tiktoken.encoding_for_model("text-embedding-ada-002")
    return num_tokens_from_string(string, encoding)
