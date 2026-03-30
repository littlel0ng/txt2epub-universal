---
name: txt2epub
description: Convert plain-text novel files into EPUB ebooks with automatic UTF-8/GBK/GB18030 decoding, Chinese chapter detection, and a client-friendly local adapter. Use when Codex needs to turn a `.txt` book or chat-uploaded novel into a structured `.epub`, or when a bot/backend needs a local TXT-to-EPUB conversion workflow.
---

# txt2epub

将 TXT 小说转换为带目录的 EPUB，并在需要时通过本地适配接口返回上层调用可直接消费的结果对象。

## Quick Start

按以下顺序执行：

1. 确认输入是本地可读的 `.txt` 文件。
2. 如果环境缺少依赖，先安装：
   ```bash
   pip3 install -r requirements.txt
   ```
3. 命令行转换：
   ```bash
   python3 scripts/convert.py <input.txt> [-o output.epub] [-a "作者"] [-t "书名"] [--pattern "自定义正则"]
   ```
4. 如果是 Bot / 自动化调用，优先使用：
   ```python
   from scripts.client_adapter import convert_for_client
   ```

## Workflow

### 1. 准备输入

- 将用户上传的 TXT 保存到本地临时路径。
- 优先保留原始文件名；如果文件名形如 `《书名》作者：作者.txt`，脚本会自动提取元数据。
- 如果输入不是 TXT，先不要调用本 skill。

### 2. 执行转换

- 常规转换直接调用 `scripts/convert.py`。
- 需要给上层程序返回结构化结果时，调用 `convert_for_client(...)`。
- 没有显式章节时，转换结果会退化为单章节 EPUB，这是预期行为。

### 3. 返回结果

- 成功时返回生成的 `.epub` 路径。
- 使用 `convert_for_client(...)` 时，返回值还包含：
  - `title`
  - `author`
  - `chapter_count`
- 上层负责把生成文件回传给用户，并清理临时文件。

## Built-in Behavior

- 自动检测 UTF-8 / UTF-8 BOM / GBK / GB18030。
- 默认章节识别覆盖：
  - `第1章`
  - `第十二回`
  - `序章` / `引子` / `楔子`
  - `Chapter 1` / `Section 1`
  - 纯数字标题
- 自动生成 TOC、spine、nav、ncx 和基础排版 CSS。
- 默认作者回退为 `Unknown`，默认标题回退为文件名 stem。

## Files

- `scripts/parser.py`
  - 编码检测与章节拆分
- `scripts/epub_builder.py`
  - 元数据提取与 EPUB 打包
- `scripts/convert.py`
  - CLI 与一站式转换入口
- `scripts/client_adapter.py`
  - 本地适配层，返回结构化结果

## Failure Handling

- 如果缺少 `ebooklib` 或 `chardet`，先安装 `requirements.txt` 中的依赖。
- 如果 TXT 文件不存在、无法解码或输出目录不可写，直接向用户返回明确错误，不要伪造成功。
- 如果章节识别不理想，可以通过 `--pattern` 或 `pattern=` 传入自定义正则。
