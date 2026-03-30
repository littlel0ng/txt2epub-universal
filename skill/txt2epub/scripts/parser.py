from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, Optional

if __package__ in {None, ""}:
    from models import Chapter
else:  # pragma: no cover
    from .models import Chapter

try:
    import chardet
except ImportError:  # pragma: no cover
    chardet = None


DEFAULT_PATTERN = (
    r"^第[0-9一二三四五六七八九十零〇百千两 ]+[章回节集卷部]"
    r"|^[Ss]ection.{1,20}$"
    r"|^[Cc]hapter.{1,20}$"
    r"|^[Pp]age.{1,20}$"
    r"|^\d{1,4}$"
    r"|^\d+、"
    r"|^引子$|^楔子$|^章节目录$|^章节$|^序章$"
)

_FALLBACK_ENCODINGS = ("utf-8-sig", "utf-8", "gb18030", "gbk")


def _normalize_detected_encoding(encoding: Optional[str]) -> Optional[str]:
    if not encoding:
        return None

    normalized = encoding.lower().replace("_", "-")
    if normalized in {"gb2312", "gbk", "gb-2312"}:
        return "gb18030"
    if normalized in {"utf-8-sig", "utf-8"}:
        return normalized
    return encoding


def _guess_encoding(sample: bytes) -> str:
    if sample.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"

    if chardet is not None:
        detected = chardet.detect(sample).get("encoding")
        normalized = _normalize_detected_encoding(detected)
        if normalized:
            return normalized

    for encoding in _FALLBACK_ENCODINGS:
        try:
            sample.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            continue

    return "utf-8"


def detect_and_read(filepath: str) -> str:
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"TXT 文件不存在: {filepath}")

    raw = path.read_bytes()
    if not raw:
        return ""

    sample = raw[:1024]
    attempted = []
    for encoding in (_guess_encoding(sample), "gb18030", "utf-8-sig", "utf-8"):
        if encoding in attempted:
            continue
        attempted.append(encoding)
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue

    raise UnicodeDecodeError(
        "txt", raw, 0, min(len(raw), 1), "无法识别文本编码，请确认文件为 UTF-8 / GBK / GB18030"
    )


def _flush_chapter(chapters: list[Chapter], title: str, lines: Iterable[str]) -> None:
    content = "\n".join(line.strip() for line in lines if line.strip()).strip()
    chapters.append(Chapter(index=len(chapters) + 1, title=title.strip(), content=content))


def parse_chapters(text: str, pattern: str = None, max_title_len: int = 35) -> list[Chapter]:
    normalized_text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized_text:
        return [Chapter(index=1, title="正文", content="")]

    chapter_pattern = re.compile(pattern or DEFAULT_PATTERN)
    chapters: list[Chapter] = []
    current_title: Optional[str] = None
    current_lines: list[str] = []
    found_any_title = False

    for raw_line in normalized_text.split("\n"):
        line = raw_line.strip()
        if not line:
            continue

        is_title = len(line) <= max_title_len and bool(chapter_pattern.match(line))
        if is_title:
            if current_title is None and current_lines:
                _flush_chapter(chapters, "前言", current_lines)
                current_lines = []
            elif current_title is not None:
                _flush_chapter(chapters, current_title, current_lines)
                current_lines = []

            current_title = line
            found_any_title = True
            continue

        current_lines.append(line)

    if current_title is not None:
        _flush_chapter(chapters, current_title, current_lines)
    elif current_lines:
        fallback_title = "正文" if not found_any_title else "尾声"
        _flush_chapter(chapters, fallback_title, current_lines)

    return chapters or [Chapter(index=1, title="正文", content=normalized_text)]
