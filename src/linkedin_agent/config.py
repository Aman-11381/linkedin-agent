import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
_project_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(_project_root / ".env")

# Azure AI Foundry — LLM project
AZURE_LLM_ENDPOINT: str = os.getenv("AZURE_LLM_ENDPOINT", "")
AZURE_LLM_API_KEY: str = os.getenv("AZURE_LLM_API_KEY", "")
AZURE_LLM_API_VERSION: str = os.getenv("AZURE_LLM_API_VERSION", "2024-12-01-preview")
LLM_DEPLOYMENT: str = os.getenv("LLM_DEPLOYMENT", "gpt-4o")

# Azure AI Foundry — Image project (can be same or different from LLM)
AZURE_IMAGE_ENDPOINT: str = os.getenv("AZURE_IMAGE_ENDPOINT", "")
AZURE_IMAGE_API_KEY: str = os.getenv("AZURE_IMAGE_API_KEY", "")
AZURE_IMAGE_API_VERSION: str = os.getenv("AZURE_IMAGE_API_VERSION", "2024-12-01-preview")
IMAGE_DEPLOYMENT: str = os.getenv("IMAGE_DEPLOYMENT", "dall-e-3")

TEMPLATES_DIR: Path = _project_root / "templates"
OUTPUT_DIR: Path = _project_root / "output"


def validate_llm() -> None:
    """Raise if LLM Azure config is missing."""
    if not AZURE_LLM_ENDPOINT:
        raise SystemExit(
            "AZURE_LLM_ENDPOINT not set. Copy .env.example to .env and add your "
            "Azure AI Foundry endpoint for the LLM project."
        )
    if not AZURE_LLM_API_KEY:
        raise SystemExit("AZURE_LLM_API_KEY not set. Add your LLM project API key to .env.")


def validate_image() -> None:
    """Raise if image Azure config is missing."""
    if not AZURE_IMAGE_ENDPOINT:
        raise SystemExit(
            "AZURE_IMAGE_ENDPOINT not set. Copy .env.example to .env and add your "
            "Azure AI Foundry endpoint for the image project."
        )
    if not AZURE_IMAGE_API_KEY:
        raise SystemExit("AZURE_IMAGE_API_KEY not set. Add your image project API key to .env.")
