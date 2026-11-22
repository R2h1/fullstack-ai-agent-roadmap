#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vault 校验器：行尾 / frontmatter schema / wikilink 断链。

用法（仓库根目录）：
    python .github/scripts/check_vault.py

任一检查失败 → 退出码 1，GitHub Actions 会把本次 push 标红。
"""
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IGNORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wikilink-ignore.txt")

# ---- canonical frontmatter schema（与 2356ad1 归一后的规范一致）------------
CANONICAL_ORDER = [
    "title", "type", "description", "target", "chapter", "chapter_title",
    "order", "week", "stage", "duration", "daily_hours", "estimated_hours",
    "reading_minutes", "difficulty", "prerequisites", "goals", "outputs",
    "tags", "prev", "next", "status", "total_files", "chapters", "created",
    "updated",
]
REQUIRED = ["title", "type", "created", "updated"]

# 明确豁免 frontmatter 的文件（仓库入口页，保持纯 README 形态）
FM_EXEMPT = {
    "README.md",
    "README.en.md",
    "README.ja.md",
}

# wikilink：[[target]] / [[target|alias]] / [[target\|alias]]（markdown 表格里竖线要转义）
WIKILINK = re.compile(r"!?\[\[([^\]\n]+)\]\]")
FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`\n]*`")


def run_git(*args):
    return subprocess.run(
        ["git", "-c", "core.quotePath=false", *args],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
    ).stdout


def md_files():
    out = run_git("ls-files", "--", "*.md")
    return [f for f in out.split("\n") if f.strip()]


def parse_frontmatter(text):
    """返回 (frontmatter_text, body, ok)。frontmatter 不存在时 ok=False。"""
    if not text.startswith("---"):
        return None, text, False
    end = text.find("\n---", 3)
    if end == -1:
        return None, text, False
    return text[3:end], text[end + 4:], True


def load_yaml_keys(fm):
    """极简 YAML 解析：只取顶层 key（够用于 schema 校验）。

    顶层 key = 行首无空白、形如 `key:` 的行。中文 key 也要抓出来，
    否则像「未知字段: x」这种拼错的字段会被静默漏过。
    """
    keys = []
    for line in fm.split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[:1].isspace():
            continue          # 嵌套内容，跳过
        m = re.match(r"^([^\s:#][^:]*):", line)
        if m:
            keys.append(m.group(1).strip())
    return keys


def strip_code(text):
    """去掉围栏代码块与行内代码，避免把示例里的 [[..]] 当成真链接。"""
    out = []
    in_fence = False
    fence_mark = ""
    for line in text.split("\n"):
        m = FENCE.match(line)
        if m:
            mark = m.group(1)
            if not in_fence:
                in_fence, fence_mark = True, mark
            elif mark == fence_mark:
                in_fence = False
            continue
        if in_fence:
            continue
        out.append(INLINE_CODE.sub("", line))
    return "\n".join(out)


def load_ignore():
    """读取显式豁免清单：每行一个链接目标，# 开头是注释。"""
    items = set()
    if os.path.exists(IGNORE_FILE):
        with io.open(IGNORE_FILE, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    items.add(line)
    return items


def main():
    errors = []
    files = md_files()
    ignore = load_ignore()
    print(f"检查 {len(files)} 个 Markdown 文件\n")

    # ---------- 1. 行尾必须是 LF ----------
    eol = run_git("ls-files", "--eol")
    for line in eol.split("\n"):
        if "w/crlf" in line:
            errors.append(f"[行尾] CRLF 工作区文件（应统一 LF）: {line.strip()}")

    # ---------- 2. frontmatter schema ----------
    stems = {}
    # 链接目标可能指向 canvas 等非 md 附件，一并纳入索引
    for rel in run_git("ls-files").split("\n"):
        rel = rel.strip()
        if not rel:
            continue
        stems[rel] = rel
        stems[os.path.splitext(rel)[0]] = rel
        stems[os.path.basename(rel)] = rel

    for rel in files:
        path = os.path.join(ROOT, rel)
        with io.open(path, encoding="utf-8") as f:
            text = f.read()
        if "\r\n" in text:
            errors.append(f"[行尾] 文件含 CRLF: {rel}")

        if os.path.basename(rel) in FM_EXEMPT:
            continue

        fm, body, ok = parse_frontmatter(text)
        if not ok:
            errors.append(f"[frontmatter] 缺少或格式错误的 frontmatter: {rel}")
            continue

        keys = load_yaml_keys(fm)
        unknown = [k for k in keys if k not in CANONICAL_ORDER]
        if unknown:
            errors.append(f"[frontmatter] 未知字段 {unknown}: {rel}")

        for req in REQUIRED:
            if req not in keys:
                errors.append(f"[frontmatter] 缺少必填字段 {req}: {rel}")

        # 顺序：canonical 字段必须按 CANONICAL_ORDER 的相对次序出现
        known = [k for k in keys if k in CANONICAL_ORDER]
        pos = [CANONICAL_ORDER.index(k) for k in known]
        if pos != sorted(pos):
            errors.append(f"[frontmatter] key 顺序不符合规范: {rel} -> {known}")

        # created / updated 必须是 YYYY-MM-DD
        for field in ("created", "updated"):
            m = re.search(rf"^{field}:\s*(\S+)", fm, re.M)
            if m and not re.match(r"^\d{4}-\d{2}-\d{2}$", m.group(1)):
                errors.append(f"[frontmatter] {field} 不是 YYYY-MM-DD ({m.group(1)}): {rel}")

    # ---------- 3. wikilink 断链 ----------
    for rel in files:
        path = os.path.join(ROOT, rel)
        with io.open(path, encoding="utf-8") as f:
            text = f.read()
        _, body, _ = parse_frontmatter(text)
        body = strip_code(body)
        rel_dir = os.path.dirname(rel)
        for raw in WIKILINK.findall(body):
            # markdown 表格里竖线被转义成 \| ，先还原别名分隔符
            target = raw.replace("\\|", "|")
            target = target.split("|")[0].strip()
            target = target.split("#")[0].strip()
            if not target or target.lower().startswith("http"):
                continue
            if target in ignore:
                continue

            candidates = [target]
            if not target.endswith(".md"):
                candidates.append(target + ".md")
            # 相对当前文件目录
            candidates.append(os.path.normpath(os.path.join(rel_dir, target)))
            if not target.endswith(".md"):
                candidates.append(os.path.normpath(os.path.join(rel_dir, target + ".md")))

            ok = False
            for c in candidates:
                if c in stems:
                    ok = True
                    break
                if c.endswith(".md") and os.path.exists(os.path.join(ROOT, c)):
                    ok = True
                    break
                # 目录形式：指向某个章节目录
                if any(st.startswith(c + "/") for st in stems):
                    ok = True
                    break
            if ok:
                continue
            # 兜底：按 basename 匹配（跨目录简写）
            base = os.path.basename(target)
            if base and (base in stems or base + ".md" in stems):
                continue
            errors.append(f"[wikilink] 断链 [[{raw.strip()}]]: {rel}")

    # ---------- 输出 ----------
    if errors:
        print(f"❌ {len(errors)} 个问题：\n")
        for e in errors:
            print("  -", e)
        print("\n若某条链接是正文里的示例而非真链接，"
              "把它加进 .github/scripts/wikilink-ignore.txt（每行一条）。")
        return 1
    print("✅ 全部通过：行尾 LF / frontmatter schema / wikilink 无断链")
    return 0


if __name__ == "__main__":
    sys.exit(main())
