---
title: 第 03 章 - HTML / CSS 现代 Web
type: chapter-outline
chapter: "03"
chapter_title: HTML / CSS 现代 Web
order: 1
duration: 4+2 周
prerequisites:
  - "[[全栈学习路线/00-学习方法论/00-学习方法论总纲]]"
  - "[[全栈学习路线/02-JavaScript-从零到源码/00-JavaScript总纲]]（建议至少学到第 06 篇 DOM——本章 demo 用到 localStorage 和 DOM；布局主体可与 02 并行）"
tags: [HTML, CSS, 前端]
prev: "[[全栈学习路线/02-JavaScript-从零到源码/11-GitHub项目精选-JavaScript]]"
next: "[[01-HTML5与可访问性]]"
created: 2026-06-19
updated: 2026-11-28
---

# 第 03 章 · HTML / CSS 现代 Web（4+2 周）

> HTML/CSS 不是"会写"就够，要做到**像素级还原 + 性能 + 可访问性**。
> ⏱️ **节奏**：4 周主线（第 01~04 篇）+ **1~2 周章项目**（还原工作流在第 04 篇 §十六，工时拆分见 §16.6）。

## 🎯 章节目标

- 写出语义化、可访问（a11y）的 HTML5
- 掌握 Flex / Grid / Container Query 等现代布局
- 会写响应式、暗黑模式、动画
- 理解浏览器渲染管线（Parse → Style → Layout → Paint → Composite）
- 掌握**像素级还原工作流**（量取 → 骨架 → tokens → 动效 → 截图验收 → 部署），独立完成 1 个真实站点的精做还原（有余力再做 2 个）
- 掌握 Tailwind CSS（2026 年事实标准）

## 📅 周计划

| # | 主题 | 关键产出 |
|---|------|----------|
| 第 01 篇 | HTML5 语义化 + 可访问性 + SEO | 个人简历页 |
| 第 02 篇 | CSS 基础 + Flex + Grid + 响应式 | 仿 GitHub 主页 |
| 第 03 篇 | CSS 进阶：变量 / 动画 / 暗黑模式 / 容器查询 / 纯 CSS 组件 | 模态框+手风琴+开关+步骤条四件套 |
| 第 04 篇 | Tailwind v4 + 渲染原理 + 性能 + 还原工作流 | 章项目 A（Linear 精做）启动 |
| 项目周（1~2 周） | §十六 工作流实战：骨架 → tokens → 动效 → 叠图验收 → Vercel 部署 | 章项目 A 交付（B/C 选做） |

## 📖 详细内容

### 第 01 篇 - HTML5
- 语义化标签（header/nav/main/article/section/aside/footer）
- 表单 + 校验（required/pattern/type）
- 可访问性 ARIA 属性 + 键盘导航
- Open Graph / Twitter Card / JSON-LD（SEO）
- （IO / ResizeObserver / Web Storage 等浏览器 API 的教学习惯在第 02 章第 06 篇，本章 demo 直接引用）

### 第 02 篇 - CSS 基础与布局
- 选择器优先级 + 继承
- 盒模型 + box-sizing
- 定位（static/relative/absolute/fixed/sticky）
- **Flexbox 完全指南**（[CSS-Tricks Flex](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)）
- **Grid 完全指南**（[CSS-Tricks Grid](https://css-tricks.com/snippets/css/complete-guide-grid/)）
- 媒体查询 + 移动优先

### 第 03 篇 - CSS 进阶
- CSS 变量 + 主题切换（暗黑模式，含 matchMedia 系统偏好检测）
- 动画：transition / @keyframes / animation
- transform 3D + will-change（性能）
- 滤镜：filter / backdrop-filter
- 现代特性：`:has()` / `@container` / `subgrid` / CSS 嵌套 / scroll-driven animations
- Logical Properties（margin-inline 等）
- 纯 CSS 组件四件套：模态框 / 手风琴 / 开关 / 步骤条（T3）
- 必读：张鑫旭《CSS 世界》《CSS 选择器世界》《CSS 新世界》

### 第 04 篇 - Tailwind + 性能
- Tailwind CSS v4 思路 + `@theme` 配置 + 最佳实践
- shadcn/ui（基于 Tailwind 的组件方案）
- 渲染管线：Parse → Style → Layout → Paint → Composite
- 重排（Reflow）vs 重绘（Repaint）vs 合成（Composite）
- Critical CSS / 字体加载策略 / 图片懒加载
- Lighthouse + Web Vitals（LCP / INP / CLS）
- **§十六 章项目集成：像素级还原工作流**（量取 / 骨架 / GSAP+Lenis / 截图对比 / 体积 / 部署）

## 📝 考核任务

- [ ] **T1**：纯 HTML 写一份语义化简历，通过 [WAVE](https://wave.webaim.org/) 0 错误（把简历页拖进 WAVE 首页的上传/URL 框即可检测；命令行党可用 `npx @axe-core/cli <url>`）
- [ ] **T2**：[Frontend Mentor](https://www.frontendmentor.io/) 完成 5 个 newbie 项目（第 02 篇先做 2 个热身，本章项目周前补齐 5 个）
- [ ] **T3**：实现仅 CSS 的：手风琴 / 模态框 / 步骤条 / 切换开关（第 03 篇 §13.1 + §十四 全有实现）
- [ ] **T4**：实现暗黑模式切换（含系统偏好检测 + 本地保存 + 平滑过渡，第 03 篇 §2.3 完整代码）
- [ ] **T5**：用 CSS Grid 复刻一份杂志排版
- [ ] **T6**：用 Tailwind 复刻 [shadcn/ui](https://ui.shadcn.com/) 中 10 个组件
- [ ] **T7**：把任意一个之前做的页面性能优化到 Lighthouse 95+

## 🚀 章节大项目：像素级还原真实站点（1 精做 + 2 选做）

> 📌 **开工前先读第 04 篇 §十六「章项目集成」**：量取工作流、骨架先行法、GSAP/Lenis 滚动动效、截图对比、体积检查、Vercel 部署——章项目要用的每一项技能都在那里给了最小实现。**精做 A 是必修**；B/C 选做，C 可以推迟到第 04 章后再回来做。

要求**不看 F12**，仅看视觉效果还原（容器宽度允许 2px 内偏差，用 §16.4 的叠图法校验）。

### 项目 A：[Linear](https://linear.app/) 落地页 ⭐必修·精做（中等难度，8-10h）
- 复杂的渐变 + 滚动动画
- 视频背景 + Hero
- 响应式（移动 + 桌面）
- **技术栈**：HTML + Tailwind CSS + 极少 JS

### 项目 B：[Stripe](https://stripe.com/) 首页（选做，高难度，6-8h）
- 双层视差滚动
- 复杂卡片悬浮动画
- 全局色彩主题切换
- **技术栈**：HTML + Tailwind + GSAP（§16.3 有最小教学）

### 项目 C：[Apple AirPods Pro](https://www.apple.com/airpods-pro/) 产品页（选做，地狱难度，12h+，可推迟到 04 章后）
- 滚动驱动的 3D 旋转/缩放
- 3-4 段视频拼接成连续滚动
- 文字与媒体的精确同步
- **技术栈**：HTML + Tailwind + Lenis（平滑滚动）+ ScrollTrigger

### 验收标准（对精做的 A 执行；B/C 完成时同样适用）
- [ ] 部署到 Vercel（§16.5 三行命令），公网可访问
- [ ] 移动端 + 平板 + 桌面三档响应式
- [ ] Lighthouse 性能 ≥ 90，可访问性 ≥ 95（100 是天花板，95 是可验收的工程目标）
- [ ] 总 JS 体积 < 100KB（gzip，§16.5 有测量法）
- [ ] 截图对比 ≥ 90% 相似：叠图法（§16.4 档位 1）即可；追求精确用 BackstopJS（§16.4 档位 2）

### 进阶挑战
- 用 Astro 做 SSG 输出
- 加 i18n 中英双语切换
- 用 [Motion One](https://motion.dev/) 替代 GSAP（更小）

## 📚 推荐资源

### 文档
- 📖 [MDN HTML/CSS（中文）](https://developer.mozilla.org/zh-CN/docs/Web)
- 📖 [web.dev/learn](https://web.dev/learn/) - Google 官方现代 Web 课
- 📖 [Tailwind 官方文档](https://tailwindcss.com/docs)（v4）

### 必读博客
- 📖 [张鑫旭博客](https://www.zhangxinxu.com/wordpress/) - 中文 CSS 第一博
- 📖 [CSS-Tricks](https://css-tricks.com/)
- 📖 [Josh Comeau Blog](https://www.joshwcomeau.com/) - 高质量交互式 CSS 教程

### 书
- 📘 《CSS 揭秘》Lea Verou
- 📘 张鑫旭《CSS 世界》三部曲

### 练习
- 🛠️ [Frontend Mentor](https://www.frontendmentor.io/) - 真实设计稿挑战
- 🛠️ [CSS Battle](https://cssbattle.dev/) - 最少代码复现 UI
- 🛠️ [100 Days CSS](https://100dayscss.com/)

### 灵感
- 🎨 [Awwwards](https://www.awwwards.com/)
- 🎨 [CodePen](https://codepen.io/)

---

✅ 章项目 A 精做完成并部署 → 进入 [[04-前端框架-React/00-React总纲]]
