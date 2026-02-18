from pathlib import Path

from jinja2 import Environment, FileSystemLoader, meta

from linkedin_agent.config import TEMPLATES_DIR


def _get_env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        keep_trailing_newline=True,
    )


def render(template_name: str, **variables: str) -> str:
    """Render a template file with the given variables."""
    env = _get_env()
    template = env.get_template(template_name)
    return template.render(**variables).strip()


def list_placeholders(template_name: str) -> set[str]:
    """Return the set of undeclared variables in a template."""
    env = _get_env()
    source = env.loader.get_source(env, template_name)[0]  # type: ignore[union-attr]
    ast = env.parse(source)
    return meta.find_undeclared_variables(ast)
