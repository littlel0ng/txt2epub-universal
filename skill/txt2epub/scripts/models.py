from dataclasses import dataclass


@dataclass(frozen=True)
class Chapter:
    index: int
    title: str
    content: str


@dataclass(frozen=True)
class BookMetadata:
    title: str
    author: str


@dataclass(frozen=True)
class ConversionResult:
    epub_path: str
    title: str
    author: str
    chapter_count: int
