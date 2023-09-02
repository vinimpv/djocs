import openai

EMBEDDING_MODEL = "text-embedding-ada-002"

class EmbeddingFailedError(Exception):
    pass

async def get_message_embedding(message: str) -> list[float]:
    query_embedding_response = await openai.Embedding.acreate(
        model=EMBEDDING_MODEL,
        input=message,
    )
    try:
        query_embedding = query_embedding_response["data"][0]["embedding"] # type: ignore
    except Exception as e:
        raise EmbeddingFailedError(f"Failed to get embedding for message: {e}") from e

    return query_embedding
