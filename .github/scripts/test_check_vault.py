#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CI 冒烟测试：确认校验器能真正抓到问题（而不是永远绿）。

在临时副本上注入 4 类错误，断言校验器全部报出来。
不修改真实仓库。
"""
import io
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CHECKER = os.path.join(HERE, "check_vault.py")


def run_checker(cwd):
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    # 跑临时副本里的 checker：它会用自身路径推导 ROOT，才能真正校验这个 fixture
    checker = os.path.join(cwd, ".github", "scripts", "check_vault.py")
    p = subprocess.run([sys.executable, checker], cwd=cwd,
                       capture_output=True, text=True, encoding="utf-8", env=env)
    return p.returncode, p.stdout


def make_fixture(tmp):
    """造一个最小 vault：git init + 两个 md + 一个豁免清单。"""
    os.makedirs(os.path.join(tmp, ".github", "scripts"), exist_ok=True)
    shutil.copy(CHECKER, os.path.join(tmp, ".github", "scripts", "check_vault.py"))
    shutil.copy(os.path.join(HERE, "wikilink-ignore.txt"),
                os.path.join(tmp, ".github", "scripts", "wikilink-ignore.txt"))
    with io.open(os.path.join(tmp, "a.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("---\ntitle: A\ntype: note\ncreated: 2026-01-01\nupdated: 2026-01-01\n---\n\n"
                "链接 [[b]]。\n")
    with io.open(os.path.join(tmp, "b.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("---\ntitle: B\ntype: note\ncreated: 2026-01-01\nupdated: 2026-01-01\n---\n\n正文\n")
    git = lambda *a: subprocess.run(["git", "-c", "core.autocrlf=false", *a],
                                    cwd=tmp, check=True, capture_output=True)
    git("init", "-q")
    git("add", "-A")
    git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "init")


def check(name, mutate, expect_substr):
    with tempfile.TemporaryDirectory() as tmp:
        make_fixture(tmp)
        mutate(tmp)
        code, out = run_checker(tmp)
        ok = code != 0 and expect_substr in out
        print(("PASS  " if ok else "FAIL  ") + name)
        if not ok:
            print("  exit code:", code)
            print("  output:\n" + out)
        return ok


def add_broken_link(tmp):
    p = os.path.join(tmp, "a.md")
    s = io.open(p, encoding="utf-8").read()
    s += "\n又断了一个 [[完全不存在的文件]]\n"
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)


def break_frontmatter(tmp):
    p = os.path.join(tmp, "a.md")
    s = io.open(p, encoding="utf-8").read()
    s = s.replace("type: note", "type: note\n未知字段: x")
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)


def remove_required(tmp):
    p = os.path.join(tmp, "a.md")
    s = io.open(p, encoding="utf-8").read()
    s = s.replace("updated: 2026-01-01\n", "")
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)


def bad_date(tmp):
    p = os.path.join(tmp, "a.md")
    s = io.open(p, encoding="utf-8").read()
    s = s.replace("updated: 2026-01-01", "updated: 2026/01/01")
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)


def crlf(tmp):
    p = os.path.join(tmp, "a.md")
    s = io.open(p, encoding="utf-8").read()
    io.open(p, "w", encoding="utf-8", newline="").write(s.replace("\n", "\r\n"))
    # 重新入索引，让 git ls-files --eol 看到 CRLF
    subprocess.run(["git", "-c", "core.autocrlf=false", "add", "-A"],
                   cwd=tmp, check=True, capture_output=True)


def key_order(tmp):
    p = os.path.join(tmp, "a.md")
    s = io.open(p, encoding="utf-8").read()
    s = s.replace("title: A\ntype: note", "type: note\ntitle: A")
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)


def main():
    results = []
    # 先验证"干净 vault"是通过的
    with tempfile.TemporaryDirectory() as tmp:
        make_fixture(tmp)
        code, out = run_checker(tmp)
        ok = code == 0
        print(("PASS  " if ok else "FAIL  ") + "干净 vault 应通过")
        if not ok:
            print(out)
        results.append(ok)

    results.append(check("断链应被检出", add_broken_link, "断链"))
    results.append(check("未知 frontmatter 字段应被检出", break_frontmatter, "未知字段"))
    results.append(check("缺必填字段应被检出", remove_required, "缺少必填字段"))
    results.append(check("日期格式错应被检出", bad_date, "不是 YYYY-MM-DD"))
    results.append(check("CRLF 应被检出", crlf, "CRLF"))
    results.append(check("key 顺序错应被检出", key_order, "key 顺序"))

    print()
    print(f"{sum(results)}/{len(results)} 通过")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
