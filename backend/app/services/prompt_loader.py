from pathlib import Path

from app.core.config import get_settings


class PromptNotFoundError(FileNotFoundError):
    pass


def load_prompt(prompt_name: str) -> str:
    settings = get_settings()
    prompt_path = Path(settings.prompts_dir) / f"{prompt_name}.txt"

    if not prompt_path.exists():
        raise PromptNotFoundError(f"Prompt '{prompt_name}' was not found at {prompt_path}")

    return prompt_path.read_text(encoding="utf-8").strip()
