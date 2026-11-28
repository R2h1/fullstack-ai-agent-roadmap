---
title: 第 04 章 - React 从使用到源码
type: chapter-outline
chapter: "04"
chapter_title: React 从使用到源码
order: 1
duration: 10+2 周
prerequisites:
  - "[[全栈学习路线/03-HTML-CSS-现代Web/00-HTML-CSS总纲]]"
tags: [React, 前端, 源码级]
prev: "[[全栈学习路线/03-HTML-CSS-现代Web/05-GitHub项目精选-CSS与设计]]"
next: "[[01-React入门与JSX]]"
created: 2026-06-19
updated: 2026-11-28
---

# 第 04 章 · React 从使用到源码（10+2 周）

> 选 React 是因为：1) 工业界占比最大；2) Anthropic/Vercel 等头部公司主推；3) 学完 React 思想，Vue/Solid 等都好懂。

## 🎯 章节目标

- 用 React 19 写出生产级应用
- 完全掌握 Hooks 心智模型 + 自定义 Hook
- 用 Next.js App Router 做 SSR/RSC
- 状态管理：Zustand / Jotai / TanStack Query
- 表单：React Hook Form + Zod
- **手写 mini-react（含 Fiber + 调度器 + Hooks）**
- 读懂 React 真实源码：reconciler / scheduler / fiber

## 📅 周计划

| # | 主题 | 难度 | 产出 |
|---|------|------|------|
| 第 01 篇 | JSX + 组件 + Props + 列表/条件渲染 | 入门 | 计算器 + Todo |
| 第 02 篇 | Hooks 全集：useState/useEffect/useRef/useMemo/useCallback | 入门→进阶 | 搜索框（防抖+transition）+ Modal |
| 第 03 篇 | 自定义 Hook + Context + useReducer | 进阶 | 主题/i18n/Auth Hook |
| 第 04 篇 | 状态管理：Zustand + TanStack Query | 进阶 | 真实 API 应用 |
| 第 05 篇 | 路由 + 表单：React Router / RHF + Zod | 进阶 | 后台管理系统 |
| 第 06 篇 | Next.js App Router + RSC + Server Action | 进阶 | 全栈博客 |
| 第 07 篇 | 测试：Vitest + Testing Library + Playwright | 进阶 | 测试套件 |
| 第 08 篇 | 性能优化：React DevTools / Profiler / 虚拟列表 | 进阶 | 性能报告 |
| 第 09 篇 | 手写 mini-react v1：JSX → Fiber → Render | 源码级 | mini-react v1 |
| 第 10 篇 | 手写 mini-react v2：Hooks + Diff + 调度器 | 源码级 | 完整 mini-react + 源码对照 |
| 项目周（2 周） | 白板 Phase 1：canvas 渲染循环 + 交互 + 撤销重做 + 导出 + E2E（自学指南=11 篇专题 2） | 综合 | 章项目 Phase 1 交付 |

## 📖 详细内容

### 第 01 篇 - JSX 与组件基础
- React 19 心智模型
- JSX 编译产物（jsx-runtime；手写篇切回 classic createElement）
- 函数组件 vs 类组件（类组件只读不写）
- Props + Children + key
- 条件 / 列表渲染最佳实践

### 第 02 篇 - Hooks 全集
- useState（函数式更新、惰性初始化）
- useEffect（依赖数组、清理函数、闭包陷阱）
- useRef（DOM 引用 + 可变值）
- useMemo / useCallback（**只在性能敏感处用**）
- useTransition / useDeferredValue（并发特性，React 18 引入）
- use Hook（React 19 新增）

### 第 03 篇 - 自定义 Hook + Context
- Context + useContext
- useReducer（复杂状态用）
- 自定义 Hook 设计原则（命名 use*、不破坏 hook 规则）
- 经典 Hook：useLocalStorage / useDebounce / useFetch / useEventListener

### 第 04 篇 - 状态管理 + 数据获取
- Zustand（最轻量，2026 主流）
- Jotai（原子化）
- TanStack Query（服务端状态）
- SWR
- 何时用 Context、何时用 Zustand、何时用 Query

### 第 05 篇 - 路由 + 表单
- React Router v6/v7（loader / action）
- React Hook Form（性能最佳）
- Zod（schema 校验）
- 文件上传 / 富文本编辑器（Tiptap）

### 第 06 篇 - Next.js
- App Router 架构
- Server Components vs Client Components
- Server Actions
- Streaming + Suspense
- 数据获取（fetch + cache）
- 部署到 Vercel

### 第 07 篇 - 测试
- Vitest 单元测试
- React Testing Library（行为驱动）
- Mock：MSW（API 拦截）
- E2E：Playwright

### 第 08 篇 - 性能优化
- React DevTools Profiler 用法
- React.memo / useMemo / useCallback 三剑客（不要滥用）
- 虚拟列表：TanStack Virtual
- Code splitting + lazy + Suspense
- 编译器优化：React Compiler（自动 memo）

### 第 09~10 篇 - 手写 mini-react（核心！）

**主线**：跟着 didact（pomb.us《Build your own React》，~300 行教学实现）从零手写——
- 第 09 篇 v1：JSX 转换 → Element Tree → Fiber Tree → Commit DOM
- 第 10 篇 v2：调度器 + Diff 算法 + Hooks 实现 + 优先级调度（lane 概念）

**二刷（承接目标 7）**：写完自己的版本后，打开卡颂 [big-react](https://github.com/BetaSu/big-react)
对照——你的 `wipRoot` ↔ 它的 `FiberRoot`，你的 `performUnitOfWork` ↔ 它的 `beginWork/completeWork`。
带着自己写的 ~500 行当地图再去读真实源码，才读得动。10 篇末尾有「源码对照表」承接带读。

**必看**：[React 技术揭秘 - 卡颂](https://react.iamkasong.com/)

## 📝 考核任务

- [ ] **T1**：实现一个 Todo 应用，含拖拽排序、过滤、本地持久化
- [ ] **T2**：实现 5 个自定义 Hook（useDebounce / useLocalStorage / useFetch / useOnClickOutside / useMediaQuery——第 03 篇 §1~§6 各有一节，全部有正文承担）
- [ ] **T3**：用 Zustand + TanStack Query 重写 T1
- [ ] **T4**：用 RHF + Zod 做一个含 10 个字段的复杂表单
- [ ] **T5**：用 Next.js App Router 做一个 SSR 博客（数据来自 markdown 文件）
- [ ] **T6**：给任意项目加测试，覆盖率 ≥ 70%
- [ ] **T7**：性能优化案例：将一个慢渲染场景从 60ms 优化到 < 16ms，写报告
- [ ] **T8**：按第 09~10 篇手写 mini-react（v1+v2），跑通 10 篇「项目验收」的 TodoApp 四条通过标志 + 周末 Checklist 全勾
- [ ] **T9**：写一篇博客《React Fiber 是什么，为什么需要它》(≥ 5000 字)
- [ ] **T10**：阅读 React 真实源码 `packages/react-reconciler/src/ReactFiberBeginWork.js`，做行级注释（注意：2024 年官方已合并 new/old 双 fork，旧资料里的 `.new.js` 后缀不复存在）

## 🚀 章节大项目：在线协作白板（Excalidraw 简化版，04+05 章联合项目）

> **范围说明**：本章正文教的是 React 全家桶，**没有教** Canvas 库（Konva/fabric）、Yjs、
> shadcn/ui、触摸事件、导出格式——这些在项目周自学（指南 = [[11-GitHub项目精选-React生态|11 篇专题 2]]）。
> **协作部分（Phase 2）依赖第 05 章后端**（WebSocket / y-websocket server），学完 05 章再回来做。
> 项目周（2 周）交付的是 Phase 1 单人白板。

### 需求
- 画矩形 / 圆 / 箭头 / 文字（Phase 1）
- 拖拽 / 缩放 / 旋转（Phase 1）
- 撤销 / 重做（Command 模式）（Phase 1）
- 导出 PNG / SVG / JSON（Phase 1）
- 多人光标 + 实时同步（用 [Yjs](https://github.com/yjs/yjs) CRDT）（**Phase 2，05 章后**）
- 房间 + 分享链接（**Phase 2，05 章后**）

### 技术栈（✅=本章正文已教，📚=项目周自学，⏳=第 05 章后）
- React 19 + TypeScript ✅（01~08 篇）
- Vite + pnpm ✅（01 篇）
- Zustand（本地状态）✅（04 篇）
- TanStack Query（服务端状态）✅（04 篇）
- Tailwind ✅（03 章）+ shadcn/ui 📚（复制粘贴组件，半天上手）
- Konva.js / fabric.js（Canvas 库，二选一）📚（11 篇专题 2 有渲染循环教学路径）
- Yjs + y-websocket（CRDT 协作）⏳
- 后端 Node.js + Hono ⏳（第 05 章《后端开发》）
- 部署：前端 Vercel ✅（06 篇），后端 Railway/Fly.io ⏳

### 验收标准

**Phase 1（04 章项目周交付）**
- [ ] 单人画板功能完整（矩形/圆/箭头/文字 + 拖拽/缩放/旋转）
- [ ] 撤销/重做无 bug（Command 模式）
- [ ] 导出 PNG / SVG 可用
- [ ] 移动端触摸可用（pointer events 统一处理）
- [ ] Lighthouse 性能 ≥ 85（08 篇工作流）
- [ ] Playwright E2E 覆盖 3 个场景：画一笔 / 撤销 / 导出（07 篇工作流）
- [ ] 前端部署 Vercel，README 含演示 GIF

**Phase 2（学完 05 章后端后回来补）**
- [ ] 双人 / 三人实时协作不冲突（Yjs + y-websocket）
- [ ] 网络抖动恢复后能自动合并
- [ ] 房间 + 分享链接，后端部署 Railway/Fly.io

### 进阶挑战
- 加 AI 智能图形识别（手绘转规范图形，07 章后可做）
- 接入 Liveblocks 替换自建后端
- 导出为可编辑的 Excalidraw 格式

## 📚 推荐资源

### 入门
- 📖 [React 中文新文档](https://zh-hans.react.dev/) - **首选，2024 重写**
- 📖 [Next.js 中文文档](https://www.nextjs.cn/)
- 📘 《React 设计原理》卡颂

### 进阶
- 📖 [Patterns.dev](https://www.patterns.dev/) - 现代 Web 模式
- 🛠️ [Bulletproof React](https://github.com/alan2207/bulletproof-react) - 工业级最佳实践
- 🛠️ [taxonomy](https://github.com/shadcn-ui/taxonomy) - shadcn 作者出品的 Next.js 模板

### 源码级
- 📖 [React 技术揭秘 - 卡颂](https://react.iamkasong.com/) - **中文最系统**
- 🛠️ [big-react](https://github.com/BetaSu/big-react) - 跟做 mini-react
- 🛠️ [react-source](https://github.com/facebook/react)
- 📖 [React 源码解读 - 贺师俊](https://github.com/AttackXiaoJinJin/reactExplain)

### 视频
- 🎥 [Theo - t3.gg](https://www.youtube.com/@t3dotgg) - 现代 React 生态
- 🎥 [Lee Robinson](https://leerob.io/) - Next.js 官方 DevRel

---

✅ 完成项目 → 进入 [[05-后端开发-FastAPI-Node/00-后端总纲]]
