from __future__ import annotations

import html
import re
import uuid
from pathlib import Path
from typing import Optional

if __package__ in {None, ""}:
    from models import BookMetadata, Chapter
else:  # pragma: no cover
    from .models import BookMetadata, Chapter

try:
    from ebooklib import epub
except ImportError:  # pragma: no cover
    epub = None


CSS_CONTENT = """
body {
  font-family: "PingFang SC", "Hiragino Sans GB", serif;
  line-height: 1.8;
  margin: 0 5%;
}
.chapter-title {
  text-align: center;
  margin: 2.5em 0 1.5em;
}
.content {
  text-indent: 2em;
  margin-top: 0;
  margin-bottom: 1em;
}
""".strip()

_TITLE_AUTHOR_PATTERN = re.compile(
    r"^《(?P<title>[^》]+)》(?:\s*作者[:：]?\s*(?P<author>.+))?$"
)
_AUTHOR_SUFFIX_PATTERN = re.compile(r"^(?P<title>.+?)(?:[-_\s]+)?作者[:：]?\s*(?P<author>.+)$")


def extract_book_metadata(
    input_path: str, title: Optional[str] = None, author: Optional[str] = None
) -> BookMetadata:
    stem = Path(input_path).stem.strip()
    parsed_title = stem
    parsed_author = "Unknown"

    for pattern in (_TITLE_AUTHOR_PATTERN, _AUTHOR_SUFFIX_PATTERN):
        match = pattern.match(stem)
        if not match:
            continue
        parsed_title = match.group("title").strip()
        parsed_author = (match.groupdict().get("author") or "Unknown").strip()
        break

    return BookMetadata(
        title=(title or parsed_title or "Untitled").strip(),
        author=(author or parsed_author or "Unknown").strip(),
    )


def _render_paragraphs(content: str) -> str:
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    if not lines:
        return ""
    return "\n".join(f'<p class="content">{html.escape(line)}</p>' for line in lines)


def _require_ebooklib() -> None:
    if epub is None:
        raise RuntimeError("缺少 ebooklib，请先执行: pip3 install -r requirements.txt")


def build_epub(
    chapters: list[Chapter],
    title: str,
    author: str = "Unknown",
    lang: str = "zh",
    output_path: str = None,
    indent: int = 2,
    align: str = "center",
) -> str:
    _require_ebooklib()
    if not chapters:
        raise ValueError("章节列表不能为空")

    output = Path(output_path) if output_path else Path.cwd() / f"{title}.epub"
    output.parent.mkdir(parents=True, exist_ok=True)

    book = epub.EpubBook()
    book.set_identifier(str(uuid.uuid4()))
    book.set_title(title)
    book.set_language(lang)
    book.add_author(author)

    effective_css = CSS_CONTENT.replace("text-indent: 2em;", f"text-indent: {indent}em;").replace(
        "text-align: center;", f"text-align: {align};"
    )
    style_item = epub.EpubItem(uid="style_book", file_name="book.css", media_type="text/css", content=effective_css)
    book.add_item(style_item)

    chapter_items = []
    for chapter in chapters:
        html_body = (
            f'<h3 class="chapter-title">{html.escape(chapter.title)}</h3>\n'
            f"{_render_paragraphs(chapter.content)}"
        )
        chapter_item = epub.EpubHtml(
            title=chapter.title,
            file_name=f"chapter_{chapter.index:03d}.xhtml",
            lang=lang,
        )
        chapter_item.content = f'<html><body>{html_body}</body></html>'
        chapter_item.add_item(style_item)
        book.add_item(chapter_item)
        chapter_items.append(chapter_item)

    book.toc = tuple(chapter_items)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav", *chapter_items]

    epub.write_epub(str(output), book, {})
    return str(output)
