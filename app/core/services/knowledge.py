import openai

SUMARIZE_TEMPLATE = """
You is a chatbot that answers questions about a project, the messages are stored in a database
for future similar questions, given the following piece of information about the project that is
stored in the followind location
KNOWLEDGE: {knowledge}
what is the summary of the knowledge? I mean extract the most important piece of information that
users would like to know about the project and produce a summary of it.
"""

async def summarize_knowledge(knowledge_content: str) -> str:
    message = SUMARIZE_TEMPLATE.format(knowledge=knowledge_content)
    result = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a world class software engineer with very good teaching skills."},
            {"role": "user", "content": message},
        ],
    )
    return result["choices"][0]["message"]["content"]
