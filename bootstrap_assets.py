from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Dict, Tuple

import requests


ASSET_CONFIG: Dict[str, Tuple[Path, str]] = {
    "database": (Path("data/ecommerce.db"), "ECOMMERCE_DB_URL"),
    "faiss_index": (Path("rag/faiss_index.bin"), "FAISS_INDEX_URL"),
    "review_chunks": (Path("rag/review_chunks.pkl"), "REVIEW_CHUNKS_URL"),
}

REQUIRED_DB_TABLES = {
    "orders",
    "order_items",
    "products",
    "customers",
    "payments",
    "reviews",
    "sellers",
}


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


def _get_asset_url(secret_name: str) -> str | None:
    return os.getenv(secret_name) or _read_streamlit_secret(secret_name)


def _download_file(url: str, target_path: Path) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, stream=True, timeout=120)
    response.raise_for_status()

    with target_path.open("wb") as file_handle:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                file_handle.write(chunk)


def _is_valid_database(asset_path: Path) -> bool:
    if not asset_path.exists() or asset_path.stat().st_size == 0:
        return False

    try:
        conn = sqlite3.connect(asset_path)
        try:
            rows = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        finally:
            conn.close()
    except sqlite3.Error:
        return False

    table_names = {row[0] for row in rows}
    return REQUIRED_DB_TABLES.issubset(table_names)


def ensure_runtime_assets() -> None:
    missing_secret_names = []

    for asset_name, (asset_path, secret_name) in ASSET_CONFIG.items():
        if asset_name == "database":
            if _is_valid_database(asset_path):
                continue
        elif asset_path.exists():
            continue

        asset_url = _get_asset_url(secret_name)
        if not asset_url:
            missing_secret_names.append(f"{asset_name}: {secret_name}")
            continue

        _download_file(asset_url, asset_path)

    if missing_secret_names:
        raise RuntimeError(
            "Missing runtime assets. Provide the required local files or set "
            "these environment variables / Streamlit secrets: "
            + ", ".join(missing_secret_names)
        )
