import datetime
from pathlib import Path

import httpx
from openai import AzureOpenAI

from linkedin_agent.config import (
    AZURE_IMAGE_API_KEY,
    AZURE_IMAGE_API_VERSION,
    AZURE_IMAGE_ENDPOINT,
    IMAGE_DEPLOYMENT,
    OUTPUT_DIR,
)


def _get_client() -> AzureOpenAI:
    return AzureOpenAI(
        azure_endpoint=AZURE_IMAGE_ENDPOINT,
        api_key=AZURE_IMAGE_API_KEY,
        api_version=AZURE_IMAGE_API_VERSION,
    )


def generate_image(prompt: str, deployment: str | None = None) -> Path:
    """Generate an image from a prompt and save it locally. Returns the file path."""
    client = _get_client()
    response = client.images.generate(
        model=deployment or IMAGE_DEPLOYMENT,
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    if not image_url:
        raise RuntimeError("Image generation returned no URL")

    # Download and save
    images_dir = OUTPUT_DIR / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = images_dir / f"linkedin_{timestamp}.png"

    resp = httpx.get(image_url, follow_redirects=True)
    resp.raise_for_status()
    file_path.write_bytes(resp.content)

    return file_path
