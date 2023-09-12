import openai
from django.conf import settings


async def get_content_embedding(content: str) -> list[float]:
    query_embedding_response = await openai.Embedding.acreate(
        model=settings.DJOCS_EMBEDDING_MODEL,
        input=content,
    )
    query_embedding = query_embedding_response["data"][0]["embedding"]  # type: ignore
    return query_embedding
