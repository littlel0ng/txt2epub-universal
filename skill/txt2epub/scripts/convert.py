from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in {None, ""}:
    SCRIPT_DIR = Path(__file__).resolve().parent
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    from epub_builder import build_epub, extract_book_metadata
    from parser import detect_and_read, parse_chapters
else:  # pragma: no cover
    from .epub_builder import build_epub, extract_book_metadata
    from .parser import detect_and_read, parse_chapters


def convert_txt_to_epub(
    input_path: str,
    output_path: str = None,
    author: str = None,
    title: str = None,
    pattern: str = None,
) -> str:
    source = Path(input_path)
    if not source.is_file():
        raise FileNotFoundError(f"TXT 文件不存在: {input_path}")

    text = detect_and_read(str(source))
    chapters = parse_chapters(text, pattern=pattern)
    metadata = extract_book_metadata(str(source), title=title, author=author)
    target = Path(output_path) if output_path else source.with_suffix(".epub")
    return build_epub(
        chapters=chapters,
        title=metadata.title,
        author=metadata.author,
        output_path=str(target),
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert TXT files into EPUB ebooks.")
    parser.add_argument("input_path", help="输入 TXT 文件路径")
    parser.add_argument("-o", "--output", dest="output_path", help="输出 EPUB 路径")
    parser.add_argument("-a", "--author", help="覆盖作者")
    parser.add_argument("-t", "--title", help="覆盖书名")
    parser.add_argument("--pattern", help="自定义章节正则")
    return parser


def main(argv: list[str] = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        result = convert_txt_to_epub(
            input_path=args.input_path,
            output_path=args.output_path,
            author=args.author,
            title=args.title,
            pattern=args.pattern,
        )
    except Exception as exc:  # pragma: no cover
        print(f"转换失败: {exc}", file=sys.stderr)
        return 1

    print(result)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
