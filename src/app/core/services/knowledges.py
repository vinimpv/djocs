from app.core.models import Knowledge
from app.core.services.embeddings import get_content_embedding
from pgvector.django import L2Distance


async def get_knowledge_embedding(knowledge: Knowledge) -> list[float]:
    content = knowledge.content
    return await get_content_embedding(content)


async def get_relevant_knowledges(
    message_embedding: list[float], user_id: str
) -> list[Knowledge]:
    knowledges_qs = (
        Knowledge.objects.annotate(distance=L2Distance("embedding", message_embedding))
        .filter(distance__lt=1, author_id=user_id)
        .order_by("distance")
    )
    knowledges = []
    async for knowledge in knowledges_qs[:2]:
        knowledges.append(knowledge)
    
    return knowledges
