---
title: VSCode 与 AI 辅助编程
type: method-guide
chapter: "00"
chapter_title: 学习方法论
order: 6
duration: 3-5 小时
difficulty: ⭐⭐
prerequisites:
  - "[[04-命令行终端基础]]"
tags: [VSCode, IDE, Cursor, Claude, AI, 提示词, 调试]
prev: "[[04-命令行终端基础]]"
next: "[[06-GitHub项目精选-入门导航]]"
created: 2026-06-19
updated: 2026-11-23
---

# VSCode 与 AI 辅助编程

> 编辑器是程序员的画板，AI 是会聊天的副驾驶。学会让它们配合你工作，而不是替你工作。

## 🎯 本章目标

- 说清 VSCode 相对其他编辑器的取舍（免费、生态、AI 支持好；代价是偶尔吃内存）
- 装好 VSCode + 15 个必装插件，并学会按需禁用而不是乱装
- 记住 20 个高频快捷键，至少熟练用上 10 个
- 会用多光标、全局搜索、集成终端三个提效功能
- 会用调试器跑通一段代码，而不是只会 `print`
- 在 Cursor / Claude Code 里选一个作为主力 AI 工具
- 掌握「15 分钟原则」，能写出 4 要素以上的提问提示词

---

## 一、为什么是 VSCode？📝

| 编辑器 | 优点 | 缺点 |
|--------|------|------|
| 记事本 | 简单 | 几乎没法写代码 |
| Sublime | 快 | 插件生态弱 |
| **VSCode** | **免费、快、生态最大、AI 支持好** | 偶尔吃内存 |
| WebStorm/PyCharm | 智能强 | 收费、较重 |
| Vim/Emacs | 极客装逼 | 学习曲线陡峭 |

**VSCode 是 2026 年最主流的编辑器**——不夸张地说，70% 的程序员在用它。

---

## 二、安装 VSCode 🚀

到 [code.visualstudio.com](https://code.visualstudio.com) 下载安装。

装完后打开终端：

```bash
code .
```

> 在某个目录运行 `code .`，就会用 VSCode 打开整个目录。**这是最常用的打开方式**。
>
> macOS 如果 `code` 命令不存在：VSCode 里按 `Cmd+Shift+P`，搜 "Shell Command: Install 'code' command in PATH"。

---

## 三、界面五大区域 🗺️

```
┌──────────────────────────────────────────────────────────┐
│ ① 活动栏 │ ② 侧边栏       │ ③ 编辑器                       │
│         │                │                              │
│ 文件     │ - src/         │  function hello() {          │
│ 搜索     │   - app.ts     │    console.log("hi");        │
│ 源代码   │ - tests/       │  }                           │
│ 调试     │                │                              │
│ 扩展     ├────────────────┼──────────────────────────────┤
│         │                │ ④ 集成终端                    │
│         │                │ $ npm run dev                │
└─────────┴────────────────┴──────────────────────────────┘
                                ⑤ 状态栏（底部）
```

| 区域 | 作用 | 快捷键 |
|------|------|--------|
| ① 活动栏 | 切换功能模块 | - |
| ② 侧边栏 | 文件树 / 搜索结果 | `Cmd+B` |
| ③ 编辑器 | 写代码 | - |
| ④ 集成终端 | 跑命令 | ``Cmd+` `` |
| ⑤ 状态栏 | Git 分支、行号、错误数 | - |

---

## 四、必装插件清单 🧩

按 `Cmd+Shift+X`（Win: `Ctrl+Shift+X`）打开扩展，搜索安装：

| 插件 | 作用 |
|------|------|
| **Chinese (Simplified) Language Pack** | 界面汉化（按需） |
| **Prettier** | 代码自动格式化 |
| **ESLint** | JavaScript 代码检查 |
| **Python**（Microsoft 官方） | Python 语言支持 |
| **Pylance** | Python 类型检查 |
| **Ruff** | 极快的 Python linter |
| **GitLens** | Git 历史追溯增强 |
| **Error Lens** | 错误信息直接显示在代码旁 |
| **Path Intellisense** | 路径自动补全 |
| **Code Spell Checker** | 拼写检查（避免变量名拼错） |
| **Better Comments** | 注释高亮（TODO / FIXME / !） |
| **Material Icon Theme** | 漂亮的文件图标 |
| **Live Server** | 一键起本地 HTTP 服务（前端用） |
| **REST Client** | 在编辑器里发 HTTP 请求 |
| **EditorConfig** | 统一团队代码风格 |

> ⚠️ 不要装一堆冗余插件，VSCode 会变慢。每装一个都要问自己：**真的需要吗？**

---

## 五、必会快捷键 20 个 ⌨️

> 下表 macOS / Windows 对照。`Cmd` 在 Win 上对应 `Ctrl`。

| # | macOS | Windows | 作用 |
|---|-------|---------|------|
| 1 | `Cmd+P` | `Ctrl+P` | 快速打开文件 🔥 |
| 2 | `Cmd+Shift+P` | `Ctrl+Shift+P` | 命令面板（万能入口） 🔥 |
| 3 | `Cmd+S` | `Ctrl+S` | 保存 |
| 4 | `Cmd+W` | `Ctrl+W` | 关闭当前标签 |
| 5 | `Cmd+B` | `Ctrl+B` | 显隐侧边栏 |
| 6 | ``Cmd+` `` | ``Ctrl+` `` | 显隐终端 🔥 |
| 7 | `Cmd+/` | `Ctrl+/` | 注释当前行 |
| 8 | `Cmd+D` | `Ctrl+D` | 选中下一个相同词（多光标） 🔥 |
| 9 | `Option+↑/↓` | `Alt+↑/↓` | 整行上移/下移 |
| 10 | `Shift+Option+↑/↓` | `Shift+Alt+↑/↓` | 复制当前行 |
| 11 | `Cmd+Shift+K` | `Ctrl+Shift+K` | 删除当前行 |
| 12 | `Cmd+F` | `Ctrl+F` | 当前文件搜索 |
| 13 | `Cmd+Shift+F` | `Ctrl+Shift+F` | 全局搜索 🔥 |
| 14 | `Cmd+Option+F` | `Ctrl+H` | 替换 |
| 15 | `F2` | `F2` | 重命名变量（智能！） 🔥 |
| 16 | `F12` | `F12` | 跳转到定义 |
| 17 | `Option+F12` | `Alt+F12` | 预览定义 |
| 18 | `Cmd+Shift+O` | `Ctrl+Shift+O` | 跳转到符号 |
| 19 | `Cmd+K Z` | `Ctrl+K Z` | 禅模式（专注写作） |
| 20 | `Cmd+Shift+L` | `Ctrl+Shift+L` | 选中所有相同词 |

🔥 = 每天会用几十次的高频快捷键，建议肌肉记忆。

### 自我检查 ✅

打开任意文件，做下面这串动作：

1. `Cmd+P` 输入文件名跳转
2. `Cmd+D` 三次连选三个相同变量
3. `F2` 重命名一个变量
4. `Cmd+/` 注释一行
5. ``Cmd+` `` 打开终端
6. `Cmd+Shift+P` 搜 "Format Document" 格式化代码

---

## 六、多光标 / 全局搜索 / 集成终端 🎯

### 多光标 —— 同时编辑多处

- `Cmd+D`：选中下一个相同词，每按一次多一个
- `Option+点击`：在任意位置加一个光标
- `Cmd+Option+↑/↓`：在上下行加光标（写表格神器）
- `Esc`：取消多光标

### 全局搜索 `Cmd+Shift+F`

支持：

- 正则（点 `.*` 图标）
- 区分大小写（点 `Aa`）
- 全词匹配（点 `ab|`）
- 限定文件类型（filter `*.py`）

### 集成终端

`` Cmd+` `` 打开。可以：

- 拆多个终端（点右上 `+`）
- 拆分屏幕（点拆分图标）
- 在 PowerShell / Bash / Zsh 之间切换

---

## 七、调试器使用基础 🐛

### 为什么不用 `print` 大法？

新手的本能：哪不对就 print 一下。能用，但慢、且会污染代码。**调试器**让你在不改代码的情况下看到任意时刻的程序状态。

### 三大概念

| 概念 | 含义 | 类比 |
|------|------|------|
| 断点 (Breakpoint) | 程序运行到这一行暂停 | 红绿灯 |
| Step Over | 走下一行 | 一步一步走 |
| Step Into | 进入函数内部 | 推门进去看 |
| Step Out | 跳出当前函数 | 出来 |
| Watch | 监视变量值 | 仪表盘 |

### 基本流程

1. 在代码行号左边点一下 → 出现红点（断点）
2. 按 `F5` 启动调试
3. 程序停在断点处
4. 用 `F10` (Step Over) / `F11` (Step Into) 单步执行
5. 鼠标悬停变量看值，或在左侧 Variables 面板看
6. `F5` 继续运行到下一个断点

🎓 学会调试器是从"业余"到"专业"的分水岭。强烈建议练熟。

---

## 八、AI 辅助编程怎么选？🤖

2026 年三大主流方案：

| 工具 | 形态 | 特点 | 适合 |
|------|------|------|------|
| **Claude Code** | 命令行 | 长任务能力强、可以自动跑命令 | 进阶/工程 |
| **Cursor** | VSCode 分支 | 编辑器原生集成、Tab 补全极强 | 日常写代码 |
| **Continue** | VSCode 插件 | 开源、可接自定义模型 | 想自托管 |
| **GitHub Copilot** | VSCode 插件 | 老牌、稳 | 单纯补全 |

### 入门推荐

- **完全新手**：Cursor（开箱即用，体验最丝滑）
- **学过基础**：Claude Code（学会"指挥 AI"是核心技能）
- **公司有合规要求**：Continue + 自部署

---

## 九、防止"AI 依赖症" 🛑

⚠️ **AI 是放大器：你强它更强；你菜它让你菜得更慢**。

零基础阶段最大的坑：什么都问 AI，结果一年下来啥也没记住。

### 15 分钟原则

> 遇到问题，先自己想/查 15 分钟再问 AI。

不是 5 分钟，不是 1 小时。15 分钟刚好够你形成"独立思考肌肉记忆"，又不会卡到崩溃。

### 三个具体做法

1. **写代码先关 AI 补全**：每天至少留 1 小时纯手写时间。
2. **AI 给的代码必须能讲出来**：每行解释给自己听，讲不出就别用。
3. **学习新概念时，先看官方文档/书，再让 AI 解释**：避免被 AI 的幻觉带偏。

### 自检 🔍

问自己：

- 离开 AI，我能写出 Hello World 吗？
- AI 给我一段代码，我能逐行说出每行在干啥吗？
- 我会自己看报错信息吗，还是无脑复制给 AI？

如果都"否"，**马上停一停，回去补基础**。

---

## 十、怎么向 AI 提问得到好答案？💬

### 提示词模板

```
[角色]：你是一名资深 Python 后端工程师。

[背景]：我在学 FastAPI，正在做一个用户登录功能。
项目结构是这样：…
当前代码是：…

[问题]：用 JWT 实现登录后，怎么在每个接口里拿到当前用户？

[约束]：
- 不要用第三方付费库
- 给出最简单的方案先，再说扩展方案
- 解释每个关键点的"为什么"，不只是"怎么做"

[期望输出]：
1. 思路总览
2. 完整可运行代码
3. 测试方法
```

记住四要素：**角色 + 背景 + 问题 + 约束**。模糊提问 = 模糊回答。

### 反面示例 ❌

```
帮我写个登录
```

→ AI 给你一坨代码，你不知道用不用得上、对不对。

### 正面示例 ✅

```
我用 Python 3.13 + FastAPI 0.165，
要写邮箱密码登录，
密码用 bcrypt 哈希存 SQLite，
登录成功返回 JWT。
请给最小可运行示例 + 5 句话说明每段在干啥。
```

→ 答案直接能用。

---

## 十一、用 AI 学习而不是抄答案 🎓

### "教学模式"提示词

> 我在学 X 概念。请用苏格拉底式提问引导我，先别给答案。每次只问我一个问题，根据我的回答决定下一步。

### "错题本"提示词

> 我刚才的代码报错是 Y。请：
> 1. 先解释这个错误的本质原因（不是表面）
> 2. 让我自己想 3 分钟该怎么改
> 3. 如果我答错，再给提示，但还是不要直接给答案

### "费曼学习法"提示词

> 我学了 Z 概念，现在我用自己的话讲一遍：[…]。
> 请你扮演不懂这个概念的学生，找出我讲解中的漏洞和错误。

---

## 十二、🐛 常见错误 🚨

先查速查表，再往下看细节。

| 错误现象 | 原因 | 解决 |
|---|---|---|
| VSCode 启动越来越慢 | 插件装太多 / 全局启用 | 禁用不用的插件（按工作区禁用，不是全局）；关掉 telemetry |
| 文件中文乱码 | 编码不是 UTF-8 | 设置搜 "encoding" 改成 `utf8`；老文件用 `iconv` 转换一次 |
| 终端提示一堆改动但你没改 | Windows CRLF vs Linux LF | **仅 Windows**：`git config --global core.autocrlf input`；**macOS / Linux 不用设**（默认就是 LF），照抄反而会出问题 |
| AI 给的代码跑不通 | 版本不匹配 | 先看版本号，把完整报错粘给 AI；三轮还修不好说明该自己读文档了 |
| 终端里敲 `code` 说找不到命令 | 没把 VSCode 加进 PATH | `Cmd+Shift+P` → "Shell Command: Install 'code' command in PATH" |
| Python 文件没有智能提示 | 没装 Python + Pylance 插件 | 装 Microsoft 官方 Python 插件和 Pylance，右下角选对解释器 |
| 调试器断点不生效 | 跑成了别的文件 / 用了 `python file.py` 而非调试模式 | 用 `Cmd+Shift+D` 打开调试面板，点「Run and Debug」 |
| VSCode 里终端是 PowerShell 但命令不认 | PowerShell 和 Bash 语法不同 | 终端右上角下拉切到 `bash` 或 `zsh` |
| 保存时自动格式化跟预期不一样 | Prettier / ESLint 规则冲突 | 项目根放 `.prettierrc` 和 `eslint.config.js` 统一规则，不要靠个人设置 |
| 主题太花看不清代码 | 装了花哨主题 | 换回 `Dark+` / `Light+`，花哨主题留给写博客截图用 |

### VSCode 启动慢

- 禁用不用的插件（按工作区禁用，不是全局）
- 关闭 telemetry：设置搜 "telemetry"

### 中文乱码

- 文件 → 偏好设置 → 设置 → 搜 "encoding" → 改为 `utf8`

### Git 提示一堆改动但你没改

通常是换行符问题（Win 的 CRLF vs Linux 的 LF）：

```bash
git config --global core.autocrlf input
```

### AI 给的代码跑不通

- 先看版本：你装的库版本和 AI 假设的可能不一样
- 把完整报错粘给 AI，让它修
- 如果三轮还修不好，**说明你应该自己读文档了**

### 终端找不到 `code` 命令

`Cmd+Shift+P` → "Shell Command: Install 'code' command in PATH"

---

## 我学完了吗？✅ checklist

- [ ] 能在终端用 `code .` 打开项目
- [ ] 装好了 Prettier + 语言相关插件
- [ ] 20 个快捷键里至少能熟练用 10 个
- [ ] 会用 `Cmd+D` 多光标编辑
- [ ] 会用 `Cmd+Shift+F` 全局搜索
- [ ] 知道断点是什么，能在 VSCode 里调试一段代码
- [ ] 选定了一个 AI 工具（Cursor / Claude Code 之一）
- [ ] 理解并实践"15 分钟原则"
- [ ] 能写出至少有 4 要素的提问提示词
- [ ] 不会无脑复制 AI 给的代码

全部打勾 → 你已具备零基础进入正式课程的全部前置条件。
进入下一章《01 - Python 从零到源码》🚀

---

## 📚 参考与延伸阅读

- 🖥️ [VS Code 官方文档 · 界面总览](https://code.visualstudio.com/docs/getstarted/userinterface)——五大区域的权威说明
- 🐞 [VS Code 调试器文档](https://code.visualstudio.com/docs/editor/debugging)——从断点到 launch.json
- ⌨️ [VS Code 基础操作](https://code.visualstudio.com/docs/editor/codebasics) / [集成终端](https://code.visualstudio.com/docs/editor/command-line)——最常用的两块
- 🧩 [写你的第一个 VS Code 扩展](https://code.visualstudio.com/api/get-started/your-first-extension)——想改造工具链时读
- 🧹 [ESLint](https://eslint.org/) / [Prettier](https://prettier.io/)——代码检查与格式化的事实标准
- 🤖 [Cursor 官方文档](https://docs.cursor.com/)——AI 编辑器选型参考
- 🤖 [Claude Code 官方文档](https://code.claude.com/docs/en/overview)——终端里的 AI 结对编程
- 🌐 [MDN Web Docs（中文）](https://developer.mozilla.org/zh-CN/)——查 Web API 行为的权威出处
