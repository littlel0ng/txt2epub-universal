from __future__ import annotations

if __package__ in {None, ""}:
    from convert import convert_txt_to_epub
    from epub_builder import extract_book_metadata
    from models import ConversionResult
    from parser import detect_and_read, parse_chapters
else:  # pragma: no cover
    from .convert import convert_txt_to_epub
    from .epub_builder import extract_book_metadata
    from .models import ConversionResult
    from .parser import detect_and_read, parse_chapters


def convert_for_client(
    input_path: str,
    output_path: str = None,
    author: str = None,
    title: str = None,
    pattern: str = None,
) -> ConversionResult:
    text = detect_and_read(input_path)
    chapters = parse_chapters(text, pattern=pattern)
    metadata = extract_book_metadata(input_path, title=title, author=author)
    epub_path = convert_txt_to_epub(
        input_path=input_path,
        output_path=output_path,
        author=metadata.author,
        title=metadata.title,
        pattern=pattern,
    )
    return ConversionResult(
        epub_path=epub_path,
        title=metadata.title,
        author=metadata.author,
        chapter_count=len(chapters),
    )
