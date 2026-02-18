from openai import AzureOpenAI

from linkedin_agent.config import (
    AZURE_LLM_API_KEY,
    AZURE_LLM_API_VERSION,
    AZURE_LLM_ENDPOINT,
    LLM_DEPLOYMENT,
)


def _get_client() -> AzureOpenAI:
    return AzureOpenAI(
        azure_endpoint=AZURE_LLM_ENDPOINT,
        api_key=AZURE_LLM_API_KEY,
        api_version=AZURE_LLM_API_VERSION,
    )


def generate_text(prompt: str, deployment: str | None = None) -> str:
    """Send a prompt to the Azure OpenAI deployment and return the generated text."""
    client = _get_client()
    response = client.chat.completions.create(
        model=deployment or LLM_DEPLOYMENT,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content or ""
