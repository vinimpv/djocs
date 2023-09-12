from app.core.models import Knowledge


async def get_context_from_knowledges(knowledges: list[Knowledge]) -> str:
    return "\n---\n".join([knowledge.content for knowledge in knowledges])
