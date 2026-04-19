from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path


DEFAULT_OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_OLLAMA_MODEL = "mistral"


def _read_streamlit_secret(name: str) -> str | None:
    project_secret_file = Path.cwd() / ".streamlit" / "secrets.toml"
    user_secret_file = Path.home() / ".streamlit" / "secrets.toml"
    if not project_secret_file.exists() and not user_secret_file.exists():
        return None

    try:
        import streamlit as st

        value = st.secrets.get(name)
        return str(value) if value else None
    except Exception:
        return None


@lru_cache(maxsize=1)
def get_ollama_url() -> str:
    return (
        os.getenv("OLLAMA_URL")
        or _read_streamlit_secret("OLLAMA_URL")
        or DEFAULT_OLLAMA_URL
    )


@lru_cache(maxsize=1)
def get_ollama_model() -> str:
    return (
        os.getenv("OLLAMA_MODEL")
        or _read_streamlit_secret("OLLAMA_MODEL")
        or DEFAULT_OLLAMA_MODEL
    )
