from __future__ import annotations

import hashlib, json, time
from pathlib import Path
from typing import Dict, Any

import yaml
from .openai_client import client, OPENAI_MODEL


class RecreateRequired(Exception):
    pass


AGENTS_DIR = Path("agents"); AGENTS_DIR.mkdir(exist_ok=True)
REGISTRY = AGENTS_DIR / "agents.json"
DOCS_DIR = Path("chatbot/documents"); DOCS_DIR.mkdir(parents=True, exist_ok=True)


def _read(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text()) if path.suffix in {".yaml", ".yml"} else json.loads(path.read_text())


def _load_cfg(name: str) -> Dict[str, Any]:
    for ext in (".yaml", ".yml", ".json"):
        cfg = _read(AGENTS_DIR / f"{name}{ext}")
        if cfg:
            return cfg
    raise FileNotFoundError


def _finger(o: Dict[str, Any]) -> str:
    return hashlib.sha1(json.dumps(o, sort_keys=True).encode()).hexdigest()


def _load_registry() -> Dict[str, Any]:
    return json.loads(REGISTRY.read_text()) if REGISTRY.exists() else {}


def _save_registry(r: Dict[str, Any]) -> None:
    REGISTRY.write_text(json.dumps(r, indent=4, ensure_ascii=False))


def _maybe_upload_pdf(cfg: Dict[str, Any], cached: Dict[str, Any]) -> tuple[list[str], str | None]:
    pdf = cfg.get("pdf")
    if not pdf:
        return [], None
    if cached.get("file_ids") and cached.get("vector_store_id"):
        return cached["file_ids"], cached["vector_store_id"]
    path = DOCS_DIR / pdf
    if not path.exists():
        return [], None
    with path.open("rb") as fp:
        fid = client.files.create(file=fp, purpose="assistants").id
    vstore = client.vector_stores.create(name=f"vs_{fid[:6]}", file_ids=[fid])
    while vstore.status != "completed":
        time.sleep(1)
        vstore = client.vector_stores.retrieve(vstore.id)
    return [fid], vstore.id


def get_or_create_agent(name: str = "general") -> Dict[str, Any]:
    registry = _load_registry()
    cached = registry.get(name, {})
    cfg = _load_cfg(name)
    cfg.setdefault("model", OPENAI_MODEL)

    file_ids, vs_id = _maybe_upload_pdf(cfg, cached)
    tools = [{"type": "file_search"}] if vs_id else []
    tool_resources = {"file_search": {"vector_store_ids": [vs_id]}} if vs_id else {}

    payload = {
        "name": cfg.get("name", name),
        "instructions": cfg.get("instructions", ""),
        "description": cfg.get("description", ""),
        "model": cfg["model"],
        "tools": tools,
        "tool_resources": tool_resources,
    }
    fp = _finger(payload)

    if cached:
        if vs_id and not cached.get("vector_store_id"):
            raise RecreateRequired
        if cached["fingerprint"] == fp:
            return cached
        client.beta.assistants.update(cached["assistant_id"], **payload)
        cached.update(fingerprint=fp, file_ids=file_ids, vector_store_id=vs_id)
        _save_registry(registry)
        return cached

    assistant = client.beta.assistants.create(**payload)
    thread_id = client.beta.threads.create().id
    registry[name] = {
        "assistant_id": assistant.id,
        "thread_id": thread_id,
        "file_ids": file_ids,
        "vector_store_id": vs_id,
        "fingerprint": fp,
    }
    _save_registry(registry)
    return registry[name]
