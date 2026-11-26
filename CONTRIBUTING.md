---
title: 贡献指南
type: overview
description: 这份学习路线的开发工作流：远程仓库配置、命名体例、frontmatter 规范、提交前校验
tags: [贡献指南, 开发流程, Git]
created: 2026-11-23
updated: 2026-11-23
---

# 🤝 贡献指南

这是一份用 Obsidian 组织的学习路线 vault（115 个 Markdown 文件）。所有内容都是 Markdown，改动门槛很低，但有几条**仓库级硬规范**必须遵守，否则 CI 会直接标红。

---

## 一、你应该怎么参与

这份路线的原始作者是 **Karovia**（[上游仓库](https://github.com/Karovia/fullstack-ai-agent-roadmap)）。本仓库是它的一个持续维护分支（[R2h1/fullstack-ai-agent-roadmap](https://github.com/R2h1/fullstack-ai-agent-roadmap)）。

三种参与方式：

| 你想做什么 | 怎么做 |
|-----------|-------|
| **提 Issue / 纠错** | 在本仓库开 Issue，说明是哪个文件哪一行、错在哪、正确的是什么 |
| **改内容** | Fork → 本地改 → 提交 → 提 PR（见下一节工作流） |
| **只读** | 直接 clone，用 Obsidian 打开 `全栈学习路线/` 目录即可 |

> ⚖️ 内容采用 **CC BY-SA 4.0**（见 [LICENSE](LICENSE)）。转载和改编请保留原作者署名，衍生作品须采用相同协议。

---

## 二、开发工作流（重点）

### 2.1 Fork + 双远程配置

你的仓库里应该有两个远程：

```
origin    →  你自己的 fork          （可推，是你的主战场）
upstream  →  Karovia 的原始仓库     （只读，用来同步上游更新）
```

标准配置：

```bash
# 1. fork 之后克隆你自己的
git clone https://github.com/<你的用户名>/fullstack-ai-agent-roadmap.git
cd fullstack-ai-agent-roadmap

# 2. 把上游加进来，命名为 upstream（只用来拉，不用来推）
git remote add upstream https://github.com/Karovia/fullstack-ai-agent-roadmap.git

# 3. 让 upstream 拒绝 push —— 防止手滑推到原作者仓库
git remote set-url --push upstream DISABLED

# 4. main 跟踪你自己的 fork，push 默认也去自己的 fork
git branch --set-upstream-to=origin/main main
git config remote.pushDefault origin
```

### 2.2 日常命令

```bash
git status                 # 看改了哪些文件
git add -A                 # 暂存
git commit -m "..."        # 提交（约定式提交，见下）
git push                   # 推到你的 fork（origin）

git fetch upstream         # 拉上游最新提交
git merge upstream/main    # 合并上游更新（有冲突就解完再提交）
```

**推之前先跑校验**（见第四节），别让 CI 替你发现。

### 2.3 分支命名

| 类型 | 命名 | 例子 |
|------|------|------|
| 修错 | `fix/<章节>-<简述>` | `fix/ch00-nvm-source` |
| 补内容 | `feat/<章节>-<简述>` | `feat/ch01-async-practice` |
| 改文档/元数据 | `docs/<简述>` | `docs/fix-readme-stats` |
| 大改 | `refactor/<范围>` | `refactor/ch08-structure` |

分支名用小写 + 短横线，不要用中文。

---

## 三、内容规范

### 3.1 章节与文件命名

- **章**：顶层目录，`00-学习方法论` 到 `09-综合实战-毕业项目`，共 10 章。
- **章节总纲**：固定占 **`00-` 槽位**，如 `00-Python总纲.md`、`00-毕业项目总纲.md`（目录名已带章号，总纲不再重复章号，避免与内容篇 `01-` 撞号）。
- **章内内容篇**：从 `01-` 排到 `NN-`，**篇号必须与总纲正文里的「第 0N 篇」一一对应**。
  - 例：`00-学习方法论/00-学习方法论总纲.md` + `01-如何高效学习编程.md` … `08-反向工程别人的代码.md`
- **改名时必须同步三处**：`wikilink`、frontmatter 的 `prev` / `next`、总纲正文里的篇号引用。漏改一处，校验器就会报断链。

### 3.2 frontmatter

每个 `.md` 文件开头必须有 frontmatter，且字段名和**顺序**都要符合 schema：

```yaml
---
title: 文件标题
type: weekly-tutorial          # 见下表
description: 一句话描述
chapter: "01"
order: 3
duration: 1 周
difficulty: ⭐⭐⭐
prerequisites: "[[上一份文件]]"
tags: [标签1, 标签2]
prev: "[[上一份文件]]"
next: "[[下一份文件]]"
created: 2026-11-23
updated: 2026-11-23
---
```

**字段顺序必须是下面这个顺序的子序列**（校验器只管名字和顺序，不管取值）：

```
title → type → description → target → chapter → chapter_title → order → week → stage
→ duration → daily_hours → estimated_hours → reading_minutes → difficulty → prerequisites
→ goals → outputs → tags → prev → next → status → total_files → chapters → created → updated
```

- **必填**：`title`、`type`、`created`、`updated`。
- `created` / `updated` 必须是 `YYYY-MM-DD`（不能带时分秒）。
- 改完文件记得同步更新 `updated`。

**`type` 常用取值**：`weekly-tutorial`（周文件）、`chapter-outline`（章总纲）、`method-guide`（方法论）、`github-curation`（GitHub 精选导航）、`resource-pack`（资源包）、`stage-doc`（阶段文档）、`tracker`（进度追踪）、`overview`（总览页）。

### 3.3 时长与难度：按类型走，别自创

| type | duration | difficulty |
|------|----------|-----------|
| `weekly-tutorial` | `7 天` / `1 周` | ⭐ / ⭐⭐ / ⭐⭐⭐ / ⭐⭐⭐⭐ / ⭐⭐⭐⭐⭐ |
| `chapter-outline` | `N 周` | 不写 |
| `method-guide` | `1 周` 或 `N-N 小时` | ⭐⭐ |
| `github-curation` | 一般不写；用 `reading_minutes` | 🌱→🌲（策展页惯例） |

**已有的惯例不是缺陷**，改之前先确认全库口径，别只改一篇造成不一致。

### 3.4 链接

- **仓库内部文件**用 Obsidian wikilink：`[[00-Python总纲]]`，带目录前缀也行：`[[全栈学习路线/01-Python-从零到源码/00-Python总纲]]`。
- **外部网址一律用普通 Markdown 链接**：`[fastapi.tiangolo.com](https://fastapi.tiangolo.com/)`。
  - ⚠️ 不要把 GitHub 仓库写成 wikilink（`[[owner/repo]]`），校验器会判成断链。
- **正文里的示例占位链接**（比如 `[[相关概念 A]]`）加进 `.github/scripts/wikilink-ignore.txt`，一行一条。

### 3.5 行尾与编码

- 全库统一 **LF**（不是 CRLF）。`.gitattributes` 里已配 `* text=auto eol=lf`。
- 如果不小心写成了 CRLF：`git add --renormalize .` 再提交。

### 3.6 提交信息（约定式提交）

```
<type>(<scope>): <简短描述>
```

`type` 取值：`docs`（文档/内容）、`fix`（修错）、`feat`（新增内容）、`refactor`（重构）、`chore`（杂务）、`ci`（流水线）、`test`（测试）、`style`（格式）。

`scope` 用章号或范围：`ch00`、`ch08`、`readme`、`ci`。

例子：

```
docs(ch00): add CLI tool exercise and align command counts
fix(ch03): correct git shortlog usage
ci: add vault check workflow
```

### 3.7 内容事实性要求（重要）

这份路线教的是**会被人照着敲的命令**，所以：

- 命令、配置项、API 名称必须**实际验证过**。写之前跑一遍，或查官方文档。
- 引用版本号要写清「截至 YYYY-MM-DD 实测」，因为版本会过期。
- 引用 GitHub 仓库的 star 数要注明是**快照**，并说明「只用来判断量级，不必深究具体数字」。
- **危险命令**（`rm -rf`、`kill -9`、删分支、删密钥）必须带 ⚠️ 提示和影响说明。

---

## 四、提交前必跑校验

```bash
python .github/scripts/check_vault.py        # 行尾 / frontmatter / wikilink 三合一
python .github/scripts/test_check_vault.py   # 校验器自测
```

全部通过才能提交。校验器检查三件事：

1. **行尾**：任何文件出现 `w/crlf` 或文件内含 `\r\n` → 失败。
2. **frontmatter**：字段名不在 schema 里、必填字段缺失、字段顺序不对、`created`/`updated` 不是 `YYYY-MM-DD` → 失败。
3. **wikilink**：指向仓库里不存在的文件 → 失败（示例占位链接走 ignore 清单豁免）。

> 💡 **新建文件后必须先 `git add` 再跑校验器** —— 校验器的文件索引取自 `git ls-files`，没被跟踪的新文件不会被检查，会导致误报断链。

CI 配置在 `.github/workflows/vault-check.yml`，push 到 `main` 或提 PR 时自动跑。

---

## 五、版本口径

全库的技术版本以 `全栈学习路线/README.md` 的「📌 版本基线」表为**唯一权威口径**。改版本时：

1. 先查官方文档确认真实最新版。
2. 同步改基线表 + 受影响的周文件。
3. 历史事实性表述**不要**改（比如「2024 年我们用的是 Python 3.10」这类有明确时间锚点的话）。

当前基线（截至 2026-11-23）：

| 领域 | 版本 |
|------|------|
| 前端 | React 19.3.x / Next.js 16.4.x（需 Node 20.9+）/ Vite 8 / TypeScript 5.1+ / Tailwind CSS v4（CSS-first） |
| 后端 | Python 3.13 / FastAPI 0.165 / Pydantic v2 / SQLAlchemy 2.0+ / Node 26 |
| 数据 | PostgreSQL 18 / Redis 8 |
| AI | LangGraph 1.x + LangChain v1（`create_agent`）/ Claude Sonnet·Haiku·Opus 5.5 / OpenAI GPT-6.2 Sol / GPT-6 Luna |

---

## 六、提 PR 之前

- [ ] `python .github/scripts/check_vault.py` 通过
- [ ] `python .github/scripts/test_check_vault.py` 通过
- [ ] 只改了自己想改的文件（`git status` 确认没带上临时文件、没误改 `.obsidian/`）
- [ ] 改了内容就更新了该文件的 `updated` 字段
- [ ] 新增文件已 `git add`
- [ ] commit message 符合约定式提交格式
- [ ] PR 描述里写清楚：**改了什么 / 为什么改 / 怎么验证的**

---

## 七、常见问题

**Q：Obsidian 里 wikilink 变成红色断链？**
A：说明目标文件名或路径改了。按 3.1 同步三处，或跑校验器看它报哪一行。

**Q：校验器报「未知字段」？**
A：frontmatter 里写了 schema 之外的字段名。要么删掉，要么把它移到正文里。

**Q：提交后 CI 红了但本地是绿的？**
A：多半是行尾。新文件忘了 `git add`，或者本地编辑器存成了 CRLF。跑 `git add --renormalize .` 再提交。

**Q：能不能改别人的仓库？**
A：不能直推上游。Fork 自己的，改完提 PR（见第二节）。

---

## 📚 相关

- [仓库 README](README.md) —— 这份路线是什么
- [章节目录](全栈学习路线/README.md) —— 10 章导航
- [学习路线全景图](全栈学习路线/学习路线全景图.md) —— 依赖关系与并行建议
- [LICENSE](LICENSE) —— CC BY-SA 4.0 全文
