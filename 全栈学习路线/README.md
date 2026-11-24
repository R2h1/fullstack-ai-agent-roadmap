---
title: 全栈 + AI Agent 学习路线总览
type: overview
target: 零基础 → 源码级精通
duration: 12-18 个月
daily_hours: 3-4
tags: [学习路线, 全栈, AI-Agent, 总览]
next: "[[INDEX]]"
status: in-progress
created: 2026-06-19
updated: 2026-11-23
---

# 🚀 全栈 + AI Agent 源码级学习路线

> **目标**：从零基础起步，最终能独立设计并实现生产级 AI Agent 全栈应用，并对 Python、JavaScript、React、LLM 等核心技术达到**源码级理解**。

## 🎯 学习哲学（先读）

1. **不要速成**：源码级精通没有捷径。你需要在"理解 → 模仿 → 重写 → 教会别人"四个阶段反复循环。
2. **项目驱动**：每章配 1 个完整项目作为验收标准，没做完项目不算学完该章。
3. **费曼学习法**：每学完一节，**在本仓库写一篇笔记教会别人**（用你自己的话）。
4. **造轮子精神**：到了源码阶段，必须亲手实现 mini 版（mini-react / mini-vue / mini-langchain）。
5. **公开学习**：把代码 push 到 GitHub，把笔记发到博客/掘金/小红书，建立反馈回路。

详见 [[00-学习方法论/00-学习方法论总纲]]

## 🗺️ 路线图（按依赖顺序）

```mermaid
graph TD
    A[00 学习方法论] --> B[01 Python 基础]
    A --> C[02 JavaScript 基础]
    B --> D[05 后端 FastAPI]
    C --> E[03 HTML/CSS]
    E --> F[04 React 前端]
    D --> G[06 数据库与工程化]
    F --> G
    D --> H[07 AI 基础 Prompt+LLM]
    B --> H
    G --> I[08 AI Agent 框架]
    H --> I
    I --> J[09 毕业项目]
```

> 06（数据库）与 07（AI 基础）是**并列的两条支线**，都汇入 08：学完 01 就可以先学 07，06 可以延后补。
> 主线串行 00→01→02→03→04→05→06→07→08→09 = 68-69 周，加上 09（8-12 周）共 **76-81 周**；并行学习 + 跳过非必需章节后实际 **12-18 个月**。

## 📚 章节索引

| # | 模块 | 周期 | 章节项目 | 状态 |
|---|------|------|----------|------|
| 00 | [[00-学习方法论/00-学习方法论总纲\|学习方法论]] | 2-3 周 | 学习仪表盘（HTML 进度页）+ 学习契约 | ⬜ |
| 01 | [[01-Python-从零到源码/01-Python总纲\|Python 从零到源码]] | 10 周 | `my-spider-cli` 异步爬虫 + PyPI 发布 | ⬜ |
| 02 | [[02-JavaScript-从零到源码/02-JavaScript总纲\|JavaScript 从零到源码]] | 10 周 | 手写 Promise / 实现 mini-lodash | ⬜ |
| 03 | [[03-HTML-CSS-现代Web/03-HTML-CSS总纲\|HTML/CSS 现代 Web]] | 4 周 | 像素级还原 3 个真实站点 | ⬜ |
| 04 | [[04-前端框架-React/04-React总纲\|React 从使用到源码]] | 10 周 | 在线协作白板 + 手写 mini-react | ⬜ |
| 05 | [[05-后端开发-FastAPI-Node/05-后端总纲\|FastAPI + Node 后端]] | 8 周 | 完整 RESTful API + JWT + 测试 | ⬜ |
| 06 | [[06-数据库与工程化/06-数据库工程化总纲\|数据库 + 工程化]] | 6 周 | `mini-twitter` 高并发短文社区 | ⬜ |
| 07 | [[07-AI基础-Prompt与LLM/07-AI基础总纲\|AI 基础：Prompt + LLM]] | 6 周 | 从零实现 GPT（rasbt 课）+ `AskMyDocs` | ⬜ |
| 08 | [[08-AI-Agent-框架与源码/08-Agent总纲\|AI Agent 框架与源码]] | 12 周 | `mini-agent-sdk` + 自建 MCP Server | ⬜ |
| 09 | [[09-综合实战-毕业项目/09-毕业项目总纲\|毕业项目]] | 8-12 周 | 一个能上线、能赚钱、能写进简历的产品 | ⬜ |

> 周期以各章实际周文件数量为准（00 为 1 周方法论章，09 为 6 个阶段文档 / 8-12 周）。

## 🛠️ 工具栈（先备齐）

| 类型 | 工具 | 备注 |
|------|------|------|
| 编辑器 | VS Code / Cursor | 必装：Python、ESLint、Prettier、GitLens |
| 终端 | iTerm2 + Oh My Zsh | macOS；Windows 用 Windows Terminal + WSL2 |
| 版本控制 | Git + GitHub | 必学，第 0 周就要会 |
| Python | uv 或 pyenv + poetry | uv 是 2025 后新标准 |
| Node.js | nvm + pnpm | pnpm 比 npm 快很多 |
| 容器 | Docker Desktop | 第 06 章用到 |
| AI 助手 | Claude / Cursor | 学习而非依赖，详见学习方法论 |
| 笔记 | Obsidian（这里！） | 边学边写笔记 |

## 📌 版本基线（全库唯一权威口径）

> 实测于 **2026-11-23**（npm / PyPI / 官方文档）。全库所有章节都以这张表为准；
> 遇到版本冲突，以本表和对应官方升级指南为准。

| 领域 | 版本基线 | 说明 |
|------|----------|------|
| Node.js | **26.x**（最新 LTS） | Next.js 16 要求 ≥ 20.9 |
| pnpm | 最新稳定版 | 配合 `corepack` 使用 |
| Python | **3.13** | 安全支持到 2029-10；新特性可用 3.14 / 3.15 |
| uv / poetry | uv 最新版 | uv 是 2025 后的新标准 |
| TypeScript | **5.1+** | Next.js 16 的最低要求 |
| React | **19.3.x** | use() / Actions / RSC 稳定 |
| React Compiler | **1.0**（已稳定） | Next 16 起 `reactCompiler: true` |
| Next.js | **16.4.x** | Turbopack 默认；middleware → proxy |
| Vite | **8.x** | 前端构建 |
| Tailwind CSS | **v4**（CSS-first） | 主题用 `@theme`，无 config.js |
| FastAPI | **0.165** | 搭配 Pydantic v2 |
| Pydantic | **v2** | v1 的 `dict()` → v2 `model_dump()` |
| SQLAlchemy | **2.0+** | 2.0 起的写法 |
| PostgreSQL | **18** | 17 仍可用；pgvector 支持 PG 13+ |
| Redis | **8** | 8.0 起为 RSALv2 / SSPLv1 / AGPLv3 三选一 |
| LangGraph | **1.x** | 配 LangChain v1 |
| LangChain | **v1** | `create_agent` 取代 `create_react_agent` |
| Claude | **Sonnet 5.5**（主）/ Haiku 5.5（廉价）/ Opus 5.5（难题） | API ID：`claude-sonnet-5-5` 等，1M 上下文 |
| OpenAI | **GPT-6.2 Sol**（日常）/ GPT-6 Luna（高吞吐） | GPT-4o 与 GPT-5 系列已弃用 |
| Claude Code / Agent SDK | 最新稳定版 | 08 章源码导读按此版本 |

> 写作教程时如果需要提到具体版本号，请从这里抄，不要凭记忆写。

## 📖 资源总库

详见 [[_资源库/资源总览]]

**必读 Top 10**（按学习顺序）：
1. [MDN Web 文档（中文）](https://developer.mozilla.org/zh-CN/)
2. [廖雪峰 Python 教程](https://liaoxuefeng.com/books/python/)
3. [现代 JavaScript 教程](https://zh.javascript.info/)
4. [阮一峰 ES6 入门](https://es6.ruanyifeng.com/)
5. 《Fluent Python (2nd)》
6. [You Don't Know JS Yet](https://github.com/getify/You-Dont-Know-JS)
7. [React 中文文档](https://zh-hans.react.dev/) + [React 技术揭秘（卡颂）](https://react.iamkasong.com/)
8. [FastAPI 中文文档](https://fastapi.tiangolo.com/zh/)
9. [Anthropic Docs](https://docs.anthropic.com/) + [Cookbook](https://github.com/anthropics/anthropic-cookbook)
10. [build-your-own-x](https://github.com/codecrafters-io/build-your-own-x)

## ✅ 进度追踪

每周日晚在 [[_我的进度追踪/周报模板]] 写一份周报，强制复盘。

每完成一个章节项目，在 [[_我的进度追踪/项目里程碑]] 打卡。

## 🔥 下一步

→ 打开 [[00-学习方法论/00-学习方法论总纲]] 开始第 0 周。
