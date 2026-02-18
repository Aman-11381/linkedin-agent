import os
import subprocess
import sys
from typing import Optional

import pyperclip
import typer
from rich.console import Console
from rich.panel import Panel

from linkedin_agent import config, templates
from linkedin_agent.image_gen import generate_image
from linkedin_agent.llm import generate_text

app = typer.Typer(
    name="agent",
    help="LinkedIn content generation CLI — posts, images, and comments.",
    no_args_is_help=True,
)
console = Console()


def _copy_to_clipboard(text: str) -> None:
    try:
        pyperclip.copy(text)
        console.print("[green]✓ Copied to clipboard[/green]")
    except pyperclip.PyperclipException:
        console.print("[yellow]⚠ Could not copy to clipboard (no clipboard tool found)[/yellow]")


# ── Post Command ─────────────────────────────────────────────────────────────


@app.command()
def post(
    topic: str = typer.Option(..., "--topic", "-t", help="Topic of the post"),
    audience: str = typer.Option(
        "software engineers and tech professionals",
        "--audience",
        "-a",
        help="Target audience",
    ),
    tone: str = typer.Option(
        "educational and engaging", "--tone", help="Tone of the post"
    ),
    key_points: Optional[str] = typer.Option(
        None, "--key-points", "-k", help="Key points to cover (optional)"
    ),
) -> None:
    """Generate a LinkedIn post from a template."""
    config.validate_llm()

    with console.status("Generating post…"):
        prompt = templates.render(
            "post.txt",
            topic=topic,
            audience=audience,
            tone=tone,
            key_points=key_points or "",
        )
        result = generate_text(prompt)

    console.print(Panel(result, title="📝 Generated Post", border_style="blue"))
    _copy_to_clipboard(result)


# ── Image Command ────────────────────────────────────────────────────────────


@app.command()
def image(
    topic: str = typer.Option(..., "--topic", "-t", help="Topic for the image"),
    style: str = typer.Option(
        "clean, modern, professional illustration",
        "--style",
        "-s",
        help="Visual style",
    ),
    description: Optional[str] = typer.Option(
        None, "--description", "-d", help="Additional image description"
    ),
    no_open: bool = typer.Option(
        False, "--no-open", help="Don't open image after generation"
    ),
) -> None:
    """Generate an image for a LinkedIn post."""
    config.validate_image()

    with console.status("Generating image…"):
        prompt = templates.render(
            "image.txt",
            topic=topic,
            style=style,
            description=description or "",
        )
        file_path = generate_image(prompt)

    console.print(f"[green]✓ Image saved to:[/green] {file_path}")

    if not no_open:
        # Open image with default viewer
        if sys.platform == "win32":
            os.startfile(file_path)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", str(file_path)], check=False)
        else:
            subprocess.run(["xdg-open", str(file_path)], check=False)


# ── Comment Command ──────────────────────────────────────────────────────────


@app.command()
def comment(
    post_text: Optional[str] = typer.Option(
        None, "--post-text", "-p", help="The LinkedIn post text to comment on"
    ),
    file: Optional[str] = typer.Option(
        None, "--file", "-f", help="Read post text from a file"
    ),
    clipboard: bool = typer.Option(
        False, "--clipboard", "-c", help="Read post text from clipboard"
    ),
    tone: str = typer.Option(
        "insightful, professional, and genuine",
        "--tone",
        help="Tone of the comment",
    ),
) -> None:
    """Generate a comment for a LinkedIn post."""
    config.validate_llm()

    # Resolve post content from one of the three input sources
    content: str | None = post_text
    if file:
        content = open(file, encoding="utf-8").read()
    elif clipboard:
        content = pyperclip.paste()

    if not content or not content.strip():
        console.print(
            "[red]Error:[/red] Provide post text via --post-text, --file, or --clipboard"
        )
        raise typer.Exit(1)

    with console.status("Generating comment…"):
        prompt = templates.render(
            "comment.txt",
            post_content=content.strip(),
            tone=tone,
        )
        result = generate_text(prompt)

    console.print(Panel(result, title="💬 Generated Comment", border_style="green"))
    _copy_to_clipboard(result)


if __name__ == "__main__":
    app()
