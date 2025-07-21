import base64
from pathlib import Path

def read_text(path: str | Path) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Erro ao ler {path}: {exc}")
        return ""


def write_text(path: str | Path, content: str) -> None:
    try:
        Path(path).write_text(content, encoding="utf-8")
    except OSError as exc:
        print(f"Erro ao escrever {path}: {exc}")


def encode_image(path: str | Path) -> str:
    with open(path, "rb") as fp:
        return base64.b64encode(fp.read()).decode()