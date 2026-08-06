from openai import OpenAI
from core.config import settings

# Initialize the OpenAI client pointing to local LMStudio
client = OpenAI(
    base_url=settings.lmstudio_base_url,
    api_key=settings.lmstudio_api_key
)

def generate_summary(query: str, context: str) -> str:
    """Sends the query and the web context to LMStudio to get a summary."""

    # 1. Put all rules and role definitions in the System Message
    system_instruction = """
    You are an expert, autonomous research assistant. 
    Your job is to read the provided context and answer the user's query comprehensively based ONLY on that context.
    """

    # 2. Put only the data (variables) in the User Message
    prompt = f"""
    User Query: {query}

    Context:
    {context}
    """

    response = client.chat.completions.create(
        model=settings.lmstudio_model, 
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content