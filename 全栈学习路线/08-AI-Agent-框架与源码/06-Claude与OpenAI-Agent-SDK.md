---
title: Claude 与 OpenAI Agent SDK
type: weekly-tutorial
chapter: "08"
chapter_title: AI Agent 框架与源码
order: 7
week: 6
estimated_hours: 14
difficulty: ⭐⭐⭐⭐
prerequisites:
  - 第 05 篇
outputs:
  - 双框架 demo
tags: [claude-agent-sdk, openai-agents-sdk, handoff, guardrail, hook, agent-sdk对比]
prev: "[[05-MCP协议详解]]"
next: "[[07-多Agent协作]]"
created: 2026-06-19
updated: 2026-11-23
---

# 第 06 篇 · Claude Agent SDK 与 OpenAI Agents SDK

> 2025 年底，Anthropic 和 OpenAI **同期推出官方 Agent SDK**。它们把第 02 篇你手写的"循环 + 工具 + handoff + guardrail"打磨成了开箱即用的库。本周对比学习两家。

---

## 一、为什么有官方 SDK？

LangGraph 是社区事实标准，但：
- 学习成本高（图、reducer、checkpointer……）
- 不少人只想"几行代码起一个 Agent"
- 官方更懂自家模型的最佳实践（streaming / cache / 工具格式）

所以两家都给出了**轻量、原厂、最佳实践**的 SDK。

---

## 二、Anthropic Claude Agent SDK

### 设计哲学

> "**把 Claude Code 的内核开放出来。**"——Anthropic, 2025

Claude Agent SDK 的循环 = Claude Code 的循环：
- 主循环 + tool_use
- 子 Agent（Task tool）
- MCP 接入
- streaming + interrupt + hook

### 安装

```bash
pip install claude-agent-sdk
# 或 TypeScript
npm i @anthropic-ai/claude-agent-sdk
```

### 最小例子（Python）

```python
import anyio
from claude_agent_sdk import query

async def main():
    async for msg in query(prompt="北京今天天气？1+2 等于几？"):
        print(msg)

anyio.run(main)
```

`query` 默认带一组**内置 tools**（read_file / write_file / bash / web_search 等，可关），跑起来就是个 mini Claude Code。

### 自定义 Tool

```python
from claude_agent_sdk import query, tool, ClaudeAgentOptions

import ast, math

_ALLOWED_NODES = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant,
                  ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod,
                  ast.Pow, ast.USub, ast.UAdd, ast.Load)

def _safe_eval(expr: str) -> float:
    """只允许四则运算——工具入参来自模型，不能裸 eval"""
    tree = ast.parse(expr, mode="eval")
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"表达式包含不允许的语法: {type(node).__name__}")
    return eval(compile(tree, "<calc>", "eval"), {"__builtins__": {}}, math.__dict__)

@tool("calc", "执行表达式", {"expr": str})
async def calc(args):
    try:
        return {"content": [{"type": "text", "text": str(_safe_eval(args["expr"]))}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"计算失败: {e}"}]}

options = ClaudeAgentOptions(
    system_prompt="你是一个严谨助理",
    tools=[calc],
    allowed_tools=["calc"],   # 关掉默认工具
    model="claude-sonnet-5-5"
)

async def main():
    async for msg in query(prompt="(1+2)*3 等于几？", options=options):
        print(msg)
```

> ⚠️ **工具安全**：Agent 的工具入参是**模型生成的**，等同于用户输入。`eval` 一次就可能执行任意代码（`__import__('os').system(...)`）。所以要么像上面那样用 `ast` 白名单把语法限死，要么改用 `simpleeval` / `sympy`，要么只暴露固定粒度的 `add/sub/mul/div` 工具。Claude Agent SDK 的 `allowed_tools` 只控制"能不能调"，**不控制"调了会不会出事"**。

### Handoff（子 Agent）

让一个 Agent 把任务交给另一个：

```python
researcher = Agent(name="researcher", system_prompt="你只查资料",
                    tools=[web_search])
writer = Agent(name="writer", system_prompt="你只写文章",
                tools=[handoff(researcher)])  # writer 可调 researcher
```

主 Agent 调研究员就像调一个工具。

### Hook（生命周期钩子）

危险操作前拦下：

```python
def before_tool(name, args):
    if name == "bash" and "rm -rf" in args.get("command", ""):
        return {"deny": True, "reason": "禁止删除"}

options = ClaudeAgentOptions(
    hooks={"pre_tool_use": before_tool}
)
```

类似 hook 还有 `pre_model`、`post_tool_use`、`on_message` 等——和 Claude Code 同一套。

### Streaming + Interrupt

```python
async for msg in query(prompt="...", options=options):
    if msg.type == "text":
        print(msg.text, end="", flush=True)
    elif msg.type == "tool_use":
        print(f"\n[调用工具] {msg.name}({msg.input})")
    # 用户按 Esc → 调 client.interrupt()
```

### 接 MCP

```python
options = ClaudeAgentOptions(
    mcp_servers={
        "obsidian": {"command": "python",
                      "args": ["/path/obsidian_mcp.py"]}
    }
)
```

Agent 启动时自动连接，所有 MCP tools 直接可用。

---

## 三、OpenAI Agents SDK

### 设计哲学

> "**Agent 是一等公民，handoff 是核心抽象，guardrail 是安全网。**"

### 安装

```bash
pip install openai-agents
# TypeScript: npm i @openai/agents
```

### 最小例子

```python
from agents import Agent, Runner

agent = Agent(
    name="Helper",
    instructions="你是一个友善助理",
    model="gpt-6.2-sol"
)

result = Runner.run_sync(agent, "你好，介绍一下自己")
print(result.final_output)
```

### 工具

```python
from agents import Agent, function_tool, Runner

@function_tool
def get_weather(city: str) -> str:
    """查天气"""
    return f"{city} 24度晴"

agent = Agent(
    name="Weatherer",
    instructions="只回答天气问题",
    tools=[get_weather]
)
print(Runner.run_sync(agent, "北京天气？").final_output)
```

### Handoff（核心抽象）

```python
from agents import Agent, handoff, Runner

billing_agent = Agent(name="Billing", instructions="只处理账单问题")
tech_agent = Agent(name="Tech", instructions="只处理技术问题")

triage = Agent(
    name="Triage",
    instructions="按用户意图把对话交给 Billing 或 Tech",
    handoffs=[billing_agent, tech_agent]
)

result = Runner.run_sync(triage, "我账单不对")
print(result.final_output)        # 由 Billing 接管后的回答
print(result.last_agent.name)     # "Billing"
```

handoff **会把完整对话历史**一起交给目标 Agent，比 Claude SDK 的 handoff 更"换人"。

### Guardrail（输入/输出守门）

```python
from agents import Agent, Runner, input_guardrail, GuardrailFunctionOutput

@input_guardrail
async def block_pii(ctx, agent, user_input: str):
    if "身份证" in user_input:
        return GuardrailFunctionOutput(
            output_info="包含 PII",
            tripwire_triggered=True
        )
    return GuardrailFunctionOutput(output_info="ok",
                                     tripwire_triggered=False)

agent = Agent(name="A", instructions="...",
                input_guardrails=[block_pii])
```

tripwire 触发时直接 raise，调用方 catch 后给用户友好提示。

### Tracing（开箱可观察）

```python
from agents import Runner, trace

with trace("my-conversation"):
    Runner.run_sync(agent, "...")
```

打开 OpenAI 平台 Traces 页面，能看到完整调用图、token、延迟、handoff 路径。

### 接 MCP

```python
from agents.mcp import MCPServerStdio

async with MCPServerStdio(
    params={"command": "python", "args": ["obsidian_mcp.py"]}
) as obs:
    agent = Agent(name="A", instructions="...", mcp_servers=[obs])
    print((await Runner.run(agent, "列我的笔记")).final_output)
```

---

## 四、两家对比表

| 维度 | Claude Agent SDK | OpenAI Agents SDK |
|---|---|---|
| 核心抽象 | `query` + tools + hooks | `Agent` + `Runner` + `handoff` |
| 心智模型 | "增强版 Claude Code" | "多 Agent + 守门 + tracing" |
| 内置工具 | read/write/bash/search 一堆 | 无（自己加） |
| Handoff | tool 形式调子 Agent | **一等公民**，状态完整迁移 |
| Guardrail | hook（pre_tool_use） | input/output guardrail |
| Tracing | 自己加 / Studio | **平台原生 Traces** |
| MCP | 原生 | 原生 |
| Streaming | 原生 | 原生 |
| Interrupt | 原生 | 通过 cancel |
| 模型 | 仅 Claude | 任意 OpenAI 兼容（含 vLLM、xAI 等） |
| 中断恢复 | session 复用 | sessions 模块 |
| 学习曲线 | 低（5 行起步） | 低（5 行起步） |

---

## 五、何时用谁？

| 场景 | 推荐 |
|---|---|
| 只用 Claude，要做"编码 / 文件操作 / 终端" Agent | **Claude Agent SDK** |
| 要灵活切换 OpenAI / 兼容模型，要 handoff | **OpenAI Agents SDK** |
| 要图式状态机、复杂分支循环 | **LangGraph** |
| 要极致定制、最小依赖 | **手写**（第 02 篇） |
| 跨厂商工具集成 | **MCP**（无关 SDK） |

---

## 六、本周实战：同一任务用三种方式做

任务：**"给我一份 X 公司的简短调研报告"**

要求：调用 web_search → 写报告 → 自我评审 → 输出 markdown。

### 实现 1：Claude Agent SDK

```python
import anyio
from claude_agent_sdk import query, tool, ClaudeAgentOptions

@tool("web_search", "搜网页", {"q": str})
async def web_search(args):
    # 调 Brave Search API（略）
    return {"content": [{"type": "text", "text": fake_search(args["q"])}]}

SYS = """你是研究员。流程：
1. 用 web_search 查公司信息（最多 3 次）
2. 写 300 字报告
3. 自我审视：信息准确否？需要再查否？
4. 终稿用 markdown 输出
"""

options = ClaudeAgentOptions(system_prompt=SYS, tools=[web_search],
                                allowed_tools=["web_search"])

async def main():
    async for msg in query(prompt="调研：Anthropic 公司", options=options):
        if msg.type == "text":
            print(msg.text, end="", flush=True)

anyio.run(main)
```

### 实现 2：OpenAI Agents SDK

```python
from agents import Agent, Runner, function_tool

@function_tool
def web_search(q: str) -> str:
    return fake_search(q)

researcher = Agent(name="Researcher",
                    instructions="查公司信息，输出 5 条要点",
                    tools=[web_search])

writer = Agent(name="Writer",
                instructions="把要点写成 300 字报告")

reviewer = Agent(name="Reviewer",
                  instructions="审稿，给 PASS 或 FAIL+理由",
                  handoffs=[writer])  # FAIL 时把任务交回 writer

main = Agent(name="Lead",
              instructions="先 handoff 给 Researcher，再交 Writer，再交 Reviewer。",
              handoffs=[researcher, writer, reviewer])

print(Runner.run_sync(main, "调研：Anthropic 公司").final_output)
```

### 对比观察

- 代码量：两家差不多
- 心智差异：Claude 偏"一个 Agent 多步走"，OpenAI 偏"多个 Agent handoff"
- 调试：OpenAI 的 Traces 页直接看图，Claude 需自加 trace

---

## 七、✅ 本周 Checklist

- [ ] Claude Agent SDK Hello world
- [ ] 自定义 tool + hook 跑通
- [ ] Claude SDK 接第 05 篇的 Obsidian MCP
- [ ] OpenAI Agents SDK Hello world
- [ ] handoff 在 Triage 里跑通
- [ ] guardrail 触发过一次 tripwire
- [ ] OpenAI Traces 平台看到调用图
- [ ] 同一调研任务两边各做一遍并对比
- [ ] 能说清 Claude 的 hook 与 OpenAI 的 guardrail 差别
- [ ] 子 Agent 只传必要上下文（成本可控，不是整段复制历史）
- [ ] 两个 SDK 各做一遍同一任务，并记下了代码量与 token 差异

---

## 八、🐛 常见错误

| 错误现象 | 原因 | 解决 |
|---|---|---|
| 自定义 tool 一直不被调用 | `allowed_tools` 没包含该工具名 | Claude 侧必须显式写 `allowed_tools=["calc"]`；OpenAI 侧确认工具已进 agent |
| handoff 了但模型还在原 Agent 跑 | handoff 工具没被触发，或描述不清 | handoff 的 description 要写清「何时移交」，并确认它在工具列表里 |
| 两个 Agent 无限互相 handoff | 没有移交次数上限 | 记录移交次数，超限强制转人工；或规定单向移交链条 |
| 成本比单 Agent 高好几倍 | 每个 Agent 都带完整 system + 全量历史 | 共享「事实层」（检索结果），各 Agent 只带自己角色片段 |
| guardrail 只挡输入不挡输出 | 只实现了输入校验 | 输入、输出双向校验（OpenAI Agents SDK 有 input / output guardrail） |
| 两家 API 写法混着来 | Claude 的 hook 与 OpenAI 的 guardrail 语义不同 | 对照 §四 的表；先只用一家跑通，再换第二家 |
| 子 Agent 的 trace 是断裂的 | 没有传递会话/用户标识 | 把 `user_id` / `thread_id` 透传给每个子 Agent，trace 才能串成树 |

---

## 九、📚 参考与延伸阅读

- Claude Agent SDK 文档与示例：<https://github.com/anthropics/claude-agent-sdk-python>
- Anthropic Claude Code SDK 文档：<https://docs.claude.com/en/docs/claude-code/sdk>
- OpenAI Agents SDK 文档（handoff / guardrail / tracing）：<https://openai.github.io/openai-agents-python>
- `openai/openai-agents-python` 仓库：<https://github.com/openai/openai-agents-python>
- 本路线第 02 篇（手写）、第 04 篇（LangGraph）、第 05 篇（MCP）

---

## 十、第 08 章总结：你现在会什么

走完第 01~06 篇：

1. **会判断**何时用 workflow / agent / 多 agent（第 01 篇）
2. **能从零手写**一个 mini-agent（第 02 篇）
3. **会用 LangGraph** 画状态机式 Agent，含 checkpointer / interrupt / streaming（第 03~04 篇）
4. **会写 MCP server** 并接到 Claude Desktop / Cursor / 自家 Agent（第 05 篇）
5. **会用官方 SDK**（Claude / OpenAI）以最少代码搭 Agent（第 06 篇）

> 这一章是整条路线的"皇冠"——后面的 RAG、Eval、生产部署，都是给这章里写出来的 Agent 加 buff。

下一章预告：**第 09 章 RAG 与向量检索**——给你的 Agent 一颗"会查资料的脑子"。
