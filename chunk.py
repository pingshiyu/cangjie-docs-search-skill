"""Load and chunk Cangjie documentation for vector and keyword search."""
from __future__ import annotations

import re
from pathlib import Path
from dataclasses import dataclass

from config import DOCS_PATH, MAX_CHUNK_CHARS, CHUNK_OVERLAP_CHARS


@dataclass
class DocChunk:
    """A chunk of documentation with metadata for retrieval."""

    id: str
    source_path: str
    title: str
    text: str

    def to_context_block(self) -> str:
        """Format chunk for LLM context (compact, with source)."""
        return f"--- Source: {self.source_path} ---\n{self.text}\n"


def collect_md_files(root: str | Path) -> list[Path]:
    """Collect all markdown files under root, excluding .git, .gitcode, and non-doc dirs."""
    root = Path(root)
    if not root.is_dir():
        return []
    skip = {".git", "node_modules", ".gitcode"}
    files = []
    for path in root.rglob("*.md"):
        if any(part in skip for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def chunk_text(text: str, max_chars: int = MAX_CHUNK_CHARS, overlap: int = CHUNK_OVERLAP_CHARS) -> list[str]:
    """Split text into overlapping chunks, preferring section boundaries (##)."""
    text = text.strip()
    if not text or len(text) <= max_chars:
        return [text] if text else []

    chunks = []
    # Split by ## headers first to get sections
    sections = re.split(r"\n(?=##\s)", text)
    current = []
    current_len = 0

    for i, section in enumerate(sections):
        section = section.strip()
        if not section:
            continue
        section_len = len(section)
        if current_len + section_len <= max_chars:
            current.append(section)
            current_len += section_len
        else:
            if current:
                combined = "\n\n".join(current)
                chunks.append(combined)
            # Start new chunk; optionally carry over overlap from end of previous
            if section_len <= max_chars:
                current = [section]
                current_len = section_len
            else:
                # Split long section by paragraphs or fixed size
                parts = _split_long_section(section, max_chars, overlap)
                for part in parts:
                    if current_len + len(part) <= max_chars:
                        current.append(part)
                        current_len += len(part)
                    else:
                        if current:
                            chunks.append("\n\n".join(current))
                        current = [part]
                        current_len = len(part)

    if current:
        chunks.append("\n\n".join(current))
    return chunks


def _split_long_section(section: str, max_chars: int, overlap: int) -> list[str]:
    """Split a long section into smaller pieces with overlap."""
    if len(section) <= max_chars:
        return [section]
    parts = []
    start = 0
    while start < len(section):
        end = start + max_chars
        if end < len(section):
            # Try to break at newline
            break_at = section.rfind("\n", start, end + 1)
            if break_at > start:
                end = break_at + 1
        parts.append(section[start:end].strip())
        start = end - overlap
        if start >= len(section):
            break
    return [p for p in parts if p]


def load_and_chunk_docs(docs_path: str | Path | None = None) -> list[DocChunk]:
    """Load all markdown files from docs path and return list of DocChunk."""
    root = Path(docs_path or DOCS_PATH)
    files = collect_md_files(root)
    chunks_out = []
    chunk_index = 0

    for path in files:
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        relative = path.relative_to(root) if root != path else path.name
        source_path = str(relative)
        # Infer title from first # line or filename
        first_line = content.split("\n")[0].strip()
        if first_line.startswith("#"):
            title = first_line.lstrip("#").strip()
        else:
            title = path.stem.replace("-", " ").replace("_", " ").title()

        for chunk_text_val in chunk_text(content):
            if not chunk_text_val.strip():
                continue
            chunk_id = f"{source_path}:{chunk_index}"
            chunks_out.append(
                DocChunk(
                    id=chunk_id,
                    source_path=source_path,
                    title=title,
                    text=chunk_text_val,
                )
            )
            chunk_index += 1

    return chunks_out


if __name__ == "__main__":
    chunks = load_and_chunk_docs()
    print(f"Loaded {len(chunks)} chunks from {DOCS_PATH}")
    if chunks:
        print("\nFirst chunk sample:")
        print(chunks[0].to_context_block()[:500], "...")
