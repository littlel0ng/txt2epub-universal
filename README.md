# txt2epub-universal

[English](#english) | [中文](#中文)

---

<h2 id="english">English</h2>

This bundle contains the portable skill `txt2epub` for OpenClaw, Codex, and Claude Desktop.

### What it does

Convert plain-text novel files into EPUB ebooks with automatic UTF-8/GBK/GB18030 decoding, Chinese chapter detection, and a client-friendly local adapter. 
Use when Codex, OpenClaw, or Claude needs to turn a `.txt` book or chat-uploaded novel into a structured `.epub`, or when a bot/backend needs a local TXT-to-EPUB conversion workflow.

### Features

- Auto-detects text encoding (UTF-8, UTF-8 BOM, GBK, GB18030).
- Automatic smart chapter recognition (e.g., Chapter 1, Section 1, Pure numeric titles, etc.).
- Automatically generates TOC, spine, nav, ncx, and basic CSS styling.
- Default author falls back to `Unknown`, title falls back to filename stem.

### Install

**OpenClaw / Codex / Claude on Windows:**
```powershell
.\install-openclaw.ps1
# OR
.\install-codex.ps1
# OR
.\install-claude.ps1
```

**OpenClaw / Codex / Claude on macOS/Linux:**
```bash
./install-openclaw.sh
# OR
./install-codex.sh
# OR
./install-claude.sh
```

---

<h2 id="中文">中文 (Chinese)</h2>

该项目包含了适用于 OpenClaw、Codex 和 Claude Desktop 的便携式技能 `txt2epub`。

### 功能介绍

将纯文本（TXT）小说文件转换为带目录的 EPUB 电子书，支持自动检测并解码 UTF-8/GBK/GB18030 编码、中文章节标题检测，以及对外部调用友好的本地适配接口。
当 Codex、OpenClaw 或 Claude 需要将聊天上传的 `.txt` 书籍转换为结构化的 `.epub` 时，或者当机器人/后端需要本地的 TXT 到 EPUB 转换工作流时，可使用该技能。

### 特性

- 自动检测并适配多种文本编码（UTF-8, UTF-8 BOM, GBK, GB18030）。
- 自动智能章节识别（如“第1章”、“第十二回”、“序章”、“Chapter 1”、纯数字标题等）。
- 自动生成目录（TOC）、spine、nav、ncx 及基础排版样式（CSS）。
- 默认作者会回退到 `Unknown`，默认标题会使用文件名。

### 安装方法

**Windows 环境下的 OpenClaw / Codex / Claude:**
```powershell
.\install-openclaw.ps1
# 或
.\install-codex.ps1
# 或
.\install-claude.ps1
```

**macOS/Linux 环境下的 OpenClaw / Codex / Claude:**
```bash
./install-openclaw.sh
# 或
./install-codex.sh
# 或
./install-claude.sh
```
