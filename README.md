# LinkedIn Agent 🚀

A CLI tool that generates LinkedIn posts, images, and comments using AI — so you can focus on ideas, not formatting.

## Quick Start

### 1. Install

```bash
cd linkedin-agent
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

pip install -e .
```

### 2. Deploy Models in Azure AI Foundry

Since gpt-4o and dall-e-3 may require different regions, they can be in separate Foundry projects:

**LLM Project** (e.g. East US):
1. Go to [Azure AI Foundry](https://ai.azure.com/) → create/open a project
2. Deploy **gpt-4o** (or your preferred chat model)
3. Note the **endpoint URL** and **API key**

**Image Project** (e.g. Sweden Central):
1. Create/open a second project in a DALL-E supported region
2. Deploy **dall-e-3**
3. Note the **endpoint URL** and **API key**

### 3. Configure

```bash
cp .env.example .env
# Edit .env and add your Azure AI Foundry settings
```

Your `.env` should look like:
```
# LLM project
AZURE_LLM_ENDPOINT=https://my-llm-resource.openai.azure.com/
AZURE_LLM_API_KEY=abc123...
LLM_DEPLOYMENT=gpt-4o

# Image project (different region)
AZURE_IMAGE_ENDPOINT=https://my-image-resource.openai.azure.com/
AZURE_IMAGE_API_KEY=def456...
IMAGE_DEPLOYMENT=dall-e-3
```

### 3. Use

#### Generate a Post

```bash
agent post --topic "CQRS Pattern" --audience "mid-level developers" --tone "educational"
```

Options:
| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--topic` | `-t` | *(required)* | Topic of the post |
| `--audience` | `-a` | `software engineers and tech professionals` | Target audience |
| `--tone` | | `educational and engaging` | Tone of the post |
| `--key-points` | `-k` | | Key points to cover |

#### Generate an Image

```bash
agent image --topic "CQRS Pattern" --style "minimalist architecture diagram"
```

Options:
| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--topic` | `-t` | *(required)* | Topic for the image |
| `--style` | `-s` | `clean, modern, professional illustration` | Visual style |
| `--description` | `-d` | | Additional details |
| `--no-open` | | `false` | Don't open image after generation |

#### Generate a Comment

```bash
# Provide text directly
agent comment --post-text "The original LinkedIn post text here..."

# Read from a file
agent comment --file post.txt

# Read from clipboard (copy a post, then run)
agent comment --clipboard
```

Options:
| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--post-text` | `-p` | | Post text to comment on |
| `--file` | `-f` | | Read post text from file |
| `--clipboard` | `-c` | | Read post text from clipboard |
| `--tone` | | `insightful, professional, and genuine` | Comment tone |

## Customizing Templates

All AI prompts live in the `templates/` directory as plain text files with Jinja2 placeholders:

- `templates/post.txt` — Post generation prompt
- `templates/image.txt` — Image generation prompt
- `templates/comment.txt` — Comment generation prompt

Edit these files to change how content is generated. Placeholders use `{{ variable_name }}` syntax. For example:

```
Write a LinkedIn post about {{ topic }} for {{ audience }}.
```

## Configuration

Environment variables (set in `.env`). LLM and image use separate Azure projects:

| Variable | Default | Description |
|----------|---------|-------------|
| `AZURE_LLM_ENDPOINT` | *(required)* | Azure endpoint for LLM project |
| `AZURE_LLM_API_KEY` | *(required)* | API key for LLM project |
| `AZURE_LLM_API_VERSION` | `2024-12-01-preview` | Azure API version for LLM |
| `LLM_DEPLOYMENT` | `gpt-4o` | Deployment name for text generation |
| `AZURE_IMAGE_ENDPOINT` | *(required)* | Azure endpoint for image project |
| `AZURE_IMAGE_API_KEY` | *(required)* | API key for image project |
| `AZURE_IMAGE_API_VERSION` | `2024-12-01-preview` | Azure API version for images |
| `IMAGE_DEPLOYMENT` | `dall-e-3` | Deployment name for image generation |

## Output

- Generated text is displayed in the terminal and **auto-copied to your clipboard**
- Generated images are saved to `output/images/` and opened automatically

## Project Structure

```
linkedin-agent/
├── .env.example        # API key template
├── pyproject.toml      # Dependencies & config
├── templates/          # Editable prompt templates
│   ├── post.txt
│   ├── image.txt
│   └── comment.txt
├── output/images/      # Generated images
└── src/linkedin_agent/
    ├── cli.py          # CLI commands
    ├── config.py       # Settings
    ├── llm.py          # Text generation
    ├── image_gen.py    # Image generation
    └── templates.py    # Template rendering
```
