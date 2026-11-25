---
title: 第 01 章 - Python 从零到源码
type: chapter-outline
chapter: "01"
chapter_title: Python 从零到源码
order: 1
duration: 10 周
prerequisites:
  - "[[全栈学习路线/00-学习方法论/00-学习方法论总纲]]"
tags: [Python, 后端, 源码级]
prev: "[[全栈学习路线/00-学习方法论/08-反向工程别人的代码]]"
next: "[[01-语法基础]]"
created: 2026-06-19
updated: 2026-11-24
---

# 第 01 章 · Python 从零到源码（10 周）

## 🎯 章节目标

学完本章你将：
- 用 Python 写出**任何**算法题、命令行工具、爬虫
- 理解装饰器、生成器、协程、元类、描述符等高级特性
- 能阅读 CPython 源码（Objects/、Modules/）
- 写出符合 PEP 8 的工程化代码（类型注解、单元测试、打包发布）

## 📅 周计划

| # | 主题 | 难度 | 关键产出 |
|---|------|------|----------|
| 第 01 篇 | 语法基础：变量/类型/运算/控制流 | 入门 | Day01-20 课后练习 |
| 第 02 篇 | 数据结构：list/tuple/dict/set + 字符串 | 入门 | LeetCode 简单 20 题 |
| 第 03 篇 | 函数 + 模块 + 文件 IO | 入门 | 命令行工具 v1（`cli-todo`，第 08/09 篇会继续在它身上改） |
| 第 04 篇 | OOP：类/继承/魔术方法/多态 | 进阶 | 自定义类库 |
| 第 05 篇 | 异常 + 装饰器 + 上下文管理器 | 进阶 | 装饰器 5 件套 |
| 第 06 篇 | 迭代器/生成器/yield from | 进阶 | 实现 itertools |
| 第 07 篇 | 并发：threading/multiprocessing/asyncio | 进阶 | 异步爬虫 |
| 第 08 篇 | 类型系统：typing + Pydantic + Protocol | 进阶 | 类型化重构 |
| 第 09 篇 | 工程化：pytest/uv/打包/发布 PyPI | 进阶 | 发一个真实包 |
| 第 10 篇 | CPython 源码导读 | 源码级 | 源码笔记 |

> **⏱️ 时间预算**：全章约 **90-120 小时**（10 周 × 每天 1.5-2 小时）。
> - **第 01~03 篇（约 25 小时）**：地基三件套 —— 语法、数据结构、函数与模块。学完能独立写出一个带测试的命令行工具（`cli-todo`）。
> - **第 04~07 篇（约 45 小时）**：Python 的「进阶四件套」—— 类、装饰器、生成器、并发。这四篇是分水岭：写得出 vs 写得好，差别就在这里。
> - **第 08~09 篇（约 20 小时）**：类型与工程化。让代码能被机器检查、被别人安装、被 CI 反复验证。
> - **第 10 篇（约 15 小时起）**：读源码。**这是最容易被低估的一段** —— 它的产出（架构图 + 博客）按「每 2 小时一个小节」推进，别指望一个周末读完。
> - **旁支 2 篇（第 11~12 篇）**：MRO 与 C3 线性化（第 10 篇的前置，建议先做）；GitHub 项目精选（全程随时查，不占整块时间）。

## 📖 详细内容大纲

### 第 01 篇 - 语法基础
- 变量、内置类型（int/float/str/bool/None）
- 算术、比较、逻辑、位运算
- if / for / while / break / continue / else
- 输入输出 `input()` / `print()` / f-string
- **必看**：[廖雪峰 Python 教程 - 基础](https://liaoxuefeng.com/books/python/basic/index.html)

### 第 02 篇 - 数据结构
- list（切片、列表推导、sort/sorted）
- tuple、namedtuple
- dict（字典推导、defaultdict、Counter、OrderedDict）
- set / frozenset
- str 详解（编码、正则）
- **必看**：[Python 官方教程 - 数据结构](https://docs.python.org/zh-cn/3/tutorial/datastructures.html)

### 第 03 篇 - 函数与模块
- 函数定义、参数（位置/关键字/默认/*args/**kwargs）
- 作用域 LEGB
- lambda + map/filter/reduce
- 模块、包、`__init__.py`、相对导入
- 文件 IO、pathlib、json/csv

### 第 04 篇 - OOP
- class、self、`__init__`
- 继承、MRO（C3 算法）、`super()`
- 魔术方法：`__repr__` / `__eq__` / `__hash__` / `__getitem__` / `__call__`
- @property / @classmethod / @staticmethod
- dataclass、enum
- 元类 metaclass、`__init_subclass__`
- 描述符协议（`__get__` / `__set__`）、数据 vs 非数据描述符
- `__slots__`
- **必读**：《Fluent Python》第 1 章 - "Python 数据模型"

### 第 05 篇 - 装饰器与上下文管理器
- 闭包 + 高阶函数
- 装饰器（无参/有参/类装饰器）
- functools.wraps / lru_cache / partial
- with 语句、`__enter__/__exit__`、contextlib
- 异常体系、自定义异常、try/except/else/finally

### 第 06 篇 - 迭代器与生成器
- 可迭代 vs 迭代器（`__iter__` / `__next__`）
- 生成器（yield）
- 协程基础（send/throw/close）
- yield from
- 实现 itertools 的 chain/islice/groupby

### 第 07 篇 - 并发
- threading + GIL 原理
- multiprocessing + Pool
- concurrent.futures
- asyncio：事件循环、协程、Task、async/await
- aiohttp / httpx 异步 HTTP

### 第 08 篇 - 类型系统
- typing：List/Dict/Optional/Union/Literal/Generic
- TypeVar、Protocol（结构化类型）
- Pydantic v2（数据验证）
- mypy 静态检查

### 第 09 篇 - 工程化
- 项目结构（src layout）
- pytest + 覆盖率
- uv（替代 pip+venv+poetry）
- ruff（替代 flake8+black+isort）
- 打包、发布到 PyPI、版本号
- pre-commit + GitHub Actions CI

### 第 10 篇 - CPython 源码导读
- CPython 整体架构（Parser → AST → Compiler → Bytecode → Eval Loop）
- `Objects/listobject.c` - list 实现
- `Objects/dictobject.c` - dict 实现（hash 冲突解决）
- `Python/ceval.c` - 字节码执行循环
- 必读：《CPython Internals》（Anthony Shaw）

### 第 11 篇 · MRO 与 C3 线性化（读源码前置）
- MRO 是什么：唯一线性列表，查找属性时沿它逐个类查
- 三条约束：子类先于父类 / 声明顺序 / 单调性
- C3 公式：`L[C] = [C] + merge(L[B1], ..., L[Bn], [B1, ..., Bn])`
- merge 的规则：每轮只取「不在任何其他序列尾部」的头部
- 手算三个例子：简单菱形 / 复杂菱形 / 无解（类定义阶段就抛 TypeError）
- 实用结论：多继承优先做成 mixin，能用组合就别用继承

### 第 12 篇 · GitHub 项目精选 · Python
- 分层浏览：🌱 入门级 / 🌿 进阶（读源码）/ 🌲 源码级 / 🛠️ 命令行·爬虫工具 / 📊 数据科学 / 💼 生产项目模板
- 项目跟读 5 步法：Find → Setup → Skim → Read → Contribute
- 7 个 Python 学习者陷阱
- 产出：跑起来 2 个、读懂 1 个、贡献 1 处

## 📝 考核任务（10 项，每周至少 1 项）

- [ ] **T1（第 01 篇）**：跟完 [Python-100-Days](https://github.com/jackfrued/Python-100-Days) 的 `Day01-20` 目录 —— 20 篇教程每天一篇，每篇末尾都有「应用练习」，至少做完 Day01-07 的全部练习
- [ ] **T2（第 02 篇）**：LeetCode 简单 20 题用 Python 通过
- [ ] **T3（第 03 篇）**：实现一个 `cli-todo` 命令行待办，支持 add/list/done/remove → 见第 03 篇「实战 4：命令行待办 cli-todo」
- [ ] **T4（第 04 篇）**：实现一个简易 `Vector` 类（支持 +、-、*、==、`__repr__`），通过《Fluent Python》第一章的所有测试
- [ ] **T5（第 05 篇）**：手写 5 个装饰器：`@timer`、`@retry`、`@cache`、`@deprecated`、`@validate_args`
- [ ] **T6（第 06 篇）**：手写一个生成器版的 `range / enumerate / zip / chain`
- [ ] **T7（第 07 篇）**：写一个异步爬虫，并发数设为 10。**验收标准用可复现的基准**：对 `httpbin.org/delay/1`（每个请求固定延迟 1 秒）发 10 个请求，总耗时 ≤ 2 秒（同步写法约 10 秒）。抓豆瓣 Top 250 只作练习用 —— 它有反爬、有随机延迟，别拿它的耗时当指标
- [ ] **T8（第 08 篇）**：用 Pydantic + typing 重写 T3 的 cli-todo，引入数据校验（add/list/done/remove 四个命令都要保留，并定义 `TodoError`/`TaskNotFound` 异常体系）
- [ ] **T9（第 09 篇）**：将 T8 打包发布到 PyPI（可用 testpypi），别人能 `pip install mytodo` 安装（包名以第 09 篇 `pyproject.toml` 里的 `name = "mytodo"` 为准）
- [ ] **T10（第 10 篇）**：阅读 `Objects/listobject.c`，画一张 PyListObject 内存布局图，写一篇 2000 字博客解析

## 🚀 章节大项目：`my-spider-cli` —— 异步并发爬虫工具

> 📌 **构建路径见第 07 篇 §11「章项目集成」**：本篇给出最小可用版（输入→并发抓→解析→输出）与逐步升级路线——第 05 篇补重试、第 08 篇补配置校验、第 09 篇补 CLI 打包与测试 CI。**学完第 07 篇即可动工，不要等全章学完。**

> 📌 **为什么叫 `my-spider-cli` 而不是 `pyspider-cli`**：PyPI 上已经有一个同名的 `pyspider-cli`（别人的包）。PyPI 的包名全局唯一，起名撞车会导致 `pip install` 装到别人的东西、或者根本发布不上去。**给自己的项目起名，习惯带上 `my-` 前缀。**

### 需求
做一个**生产级**的命令行爬虫工具，能：
1. 输入 URL 列表（文件或 stdin）
2. 异步并发抓取（可配置并发数）
3. 自动重试 + 限速
4. 解析 HTML（BeautifulSoup 或 lxml）
5. 输出 JSON / CSV
6. 进度条（rich）+ 日志（loguru）
7. 配置用 YAML，校验用 Pydantic
8. 全量类型注解 + 90% 测试覆盖率
9. 打包发布到 PyPI

### 技术栈
- Python 3.13+
- httpx（异步 HTTP）
- asyncio
- BeautifulSoup4
- click（CLI 框架；第 09 篇的打包实战用它。想更省事可以换 typer —— 它是 click 的类型标注友好版）
- rich（进度条 / 表格输出）
- loguru（日志）
- pydantic v2（配置 + 数据模型）
- pytest + pytest-asyncio + pytest-cov
- ruff + mypy
- uv（包管理）

### 验收标准
- [ ] `pip install my-spider-cli` 后能直接 `my-spider crawl urls.txt -c 10 -o out.json`
- [ ] 100 个 URL 在 5 秒内完成（依赖网速）
- [ ] 单元测试覆盖率 ≥ 85%
- [ ] mypy --strict 0 错误
- [ ] README 完整（中英双语 + 截图 GIF）
- [ ] GitHub Actions 自动跑测试 + 发版
- [ ] 至少 1 个真实抓取案例（如：豆瓣 / Hacker News / GitHub Trending）

### 进阶挑战
- 加入 Playwright 支持渲染 JS 网站
- 实现一个简易的"调度器"（去重 + 队列）
- 加入 SQLite/Redis 持久化

## 🔁 元能力复查节点（每学完一周回来看一次）

Python 是**手感语言** —— 不写就退步，写得不复习也会退回"能跑就行"。这一章学的不是一次性知识，是一套**要持续练的手艺**。所以下面这些节点不是可选项：

| 什么时候 | 花 30 分钟做什么 | 在哪看 |
|---------|----------------|--------|
| 每学完一周 | 回看这一周的实战产出：跑一遍、读一遍自己的代码，问"这段现在还满意吗？" | 本篇的实战产物 |
| 每学完一章 | 更新你的学习进度 + 写下"这章我真正会的是 ___ / 还不会的是 ___" | `my-fullstack-journey` 仓库 |
| 每月最后一个周日 | 翻一遍 Atomic Note，**删掉 1/3**（过时的、抄来的、没实践过的），补充剩下的 | Obsidian |
| 每季度 | 重读 T1-T10 的验收标准，**重做一个已经做过的任务**（不看笔记），看自己还记得多少 | 本章考核任务清单 |

> 📌 **为什么 Python 尤其需要这一节**：语法忘得快（IDE 一补全就想不起来），但设计能力不会忘 —— 只要你还在写代码、还在 review 别人的代码，装饰器和生成器的思维就会一直在。**你要复习的不是语法，是"我能不能讲清楚我为什么这么写"。**
>
> ⚠️ **第 10 篇的源码笔记是最容易烂尾的产出**。读完当天写 2000 字，和三个月后补 2000 字，价值差 10 倍。**读完一节就写一节。**

## 🐍 源码级延伸（第 10 篇之后可做）

- 用 Python 实现一个 [yet-another-Python-interpreter](https://github.com/python/cpython)（解释器子集）
- 阅读 [PEP 8](https://peps.python.org/pep-0008/) / [PEP 20](https://peps.python.org/pep-0020/) / [PEP 484](https://peps.python.org/pep-0484/) / [PEP 492](https://peps.python.org/pep-0492/)
- 给 CPython 提一个文档级 PR

## 📚 推荐资源

### 入门
- 📖 [廖雪峰 Python 教程](https://liaoxuefeng.com/books/python/) - 中文最佳入门
- 📖 [Python 官方中文教程](https://docs.python.org/zh-cn/3/tutorial/)
- 📘 《Python 编程：从入门到实践》(Eric Matthes)

### 进阶
- 📘 《Fluent Python (2nd)》Luciano Ramalho - **必读**
- 📘 《Effective Python (3rd)》Brett Slatkin
- 📖 [Real Python](https://realpython.com/) - 高质量专题文章
- 📖 [Python Cookbook 中文版](https://github.com/yidao620c/python3-cookbook)

### 源码级
- 📘 《CPython Internals》Anthony Shaw - 唯一系统讲解释器实现
- 🔗 [CPython 源码](https://github.com/python/cpython)
- 📖 [PEP 索引](https://peps.python.org/)
- 📖 [Python Language Reference](https://docs.python.org/zh-cn/3/reference/)

### 项目实战
- 🛠️ [Python-100-Days](https://github.com/jackfrued/Python-100-Days) ~188k star（2026-11-23 实测）
- 🛠️ [build-your-own-x](https://github.com/codecrafters-io/build-your-own-x)

---

✅ 完成全部 10 项考核 + 章节项目 → 进入 [[02-JavaScript-从零到源码/02-JavaScript总纲]]
