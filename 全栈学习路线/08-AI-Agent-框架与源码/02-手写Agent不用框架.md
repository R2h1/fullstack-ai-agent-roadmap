---
title: 手写 Agent，不用框架
type: weekly-tutorial
chapter: "08"
chapter_title: AI Agent 框架与源码
order: 3
week: 2
estimated_hours: 18
difficulty: ⭐⭐⭐⭐
prerequisites:
  - 第 01 篇
outputs:
  - mini-agent
tags: [agent, from-scratch, anthropic-sdk, tool-use, mini-agent]
prev: "[[01-Agent全景与5模式]]"
next: "[[03-LangGraph入门]]"
created: 2026-06-19
updated: 2026-11-23
---

# 第 02 篇 · 手写 Agent，不用框架

> 这一周你将**完全不用 LangGraph、不用任何 Agent 框架**，从 0 写一个约 300 行的 mini-agent，跑通 Claude Code 同款的"思考-工具-循环"内核。

**为什么要这么做？**
- 框架是一层抽象，**不亲手写一遍永远不知道里面在干什么**。
- 你看不懂 LangGraph 的源码，往往是因为不知道它在包装什么。
- 手写一遍后，你会惊讶："框架不过如此"。

读完这周，你能回答：
1. Agent 主循环到底循环什么？
2. tool_use 在 message 里长什么样？
3. 流式 + tool_use 怎么处理？
4. 历史压缩、错误重试、成本控制、人工审批 hook 在哪里加？

---

## 一、Agent 核心循环骨架（30 秒看懂）

```python
while True:
    response = llm.create(messages=messages, tools=tools)
    messages.append(assistant_message_from(response))

    if response.stop_reason == "end_turn":
        return  # 模型说"我做完了"

    # 模型要求调工具
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            result = execute(block.name, block.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result
            })
    messages.append({"role": "user", "content": tool_results})
```

**就这 10 行**。下面我们一版一版加功能。

---

## 二、第 1 版：单工具 Calculator Agent

```python
# v1_calculator.py
import os, json
from anthropic import Anthropic

client = Anthropic()
MODEL = "claude-sonnet-5-5"

TOOLS = [{
    "name": "calculator",
    "description": "执行数学表达式，例如 '1+2*3'",
    "input_schema": {
        "type": "object",
        "properties": {"expr": {"type": "string"}},
        "required": ["expr"]
    }
}]

def run_tool(name, args):
    if name == "calculator":
        # ⚠️ 这里为了讲清楚流程用了裸 eval；生产环境必须换成安全求值（见下方提示）
        return str(eval(args["expr"]))
    return f"unknown tool: {name}"

def agent(user_msg: str):
    messages = [{"role": "user", "content": user_msg}]
    while True:
        r = client.messages.create(
            model=MODEL, max_tokens=1024, tools=TOOLS, messages=messages
        )
        messages.append({"role": "assistant", "content": r.content})

        if r.stop_reason == "end_turn":
            # 找文本块输出
            return "".join(b.text for b in r.content if b.type == "text")

        # 处理 tool_use
        tool_results = []
        for b in r.content:
            if b.type == "tool_use":
                result = run_tool(b.name, b.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": b.id,
                    "content": result
                })
        messages.append({"role": "user", "content": tool_results})

if __name__ == "__main__":
    print(agent("(123 + 456) * 7 是多少？"))
```

跑一下，你会看到 Claude 主动调了 `calculator`，再回答你。

---

## 三、第 2 版：多工具 + 并行调用

Claude 一次可以返回多个 `tool_use` 块（并行调用）。

```python
TOOLS = [
    {"name": "calculator", "description": "...", "input_schema": {...}},
    {"name": "get_weather", "description": "查天气",
     "input_schema": {
         "type": "object",
         "properties": {"city": {"type": "string"}},
         "required": ["city"]
     }},
]

def run_tool(name, args):
    if name == "calculator": return str(eval(args["expr"]))
    if name == "get_weather": return f"{args['city']} 24度晴"
    return "unknown"
```

> ⚠️ **本节为了讲透最小流程，两处 `eval` 写得极简，生产必须加固**。工具入参来自**模型生成**，等同用户输入；一次 `eval("__import__('os').system('...')")` 就能执行任意代码。两种改法：
> 1. 用 `ast` 白名单把表达式限死在四则运算（完整可复制代码见 [[03-LangGraph入门]] 的 `_safe_eval`）；
> 2. 更推荐：干脆不给模型"算任意表达式"的能力，只暴露固定粒度的 `add/sub/mul/div` 工具 —— **能力最小化比事后过滤更安全**。

主循环不变——一次返回多个 `tool_use`，遍历执行即可。提问 "北京和上海各 24 度还是 25 度？哪个更凉？" 时，Claude 会**同一回合**返回两个 `get_weather` 调用。

---

## 四、第 3 版：加 system prompt

```python
SYSTEM = """你是一个严谨的助理。规则：
1. 不知道答案就说不知道，不要瞎编。
2. 调工具前先告诉用户你要做什么。
3. 工具失败时换思路再试。
"""

r = client.messages.create(
    model=MODEL, max_tokens=1024,
    system=SYSTEM, tools=TOOLS, messages=messages
)
```

System prompt 是**控制 Agent 性格和边界**的最直接手段。

---

## 五、第 4 版：错误重试

```python
import time

def safe_run(name, args, retries=2):
    for i in range(retries + 1):
        try:
            return run_tool(name, args)
        except Exception as e:
            if i == retries:
                return f"ERROR: {e}"  # 把错误塞回给 LLM，让它自己决定下一步
            time.sleep(1.5 ** i)
```

**关键**：错误也是给 LLM 看的"工具结果"。LLM 看到 ERROR 会自己换思路。

---

## 六、第 5 版：流式（streaming）+ tool_use 块

```python
def agent_stream(user_msg):
    messages = [{"role": "user", "content": user_msg}]
    while True:
        with client.messages.stream(
            model=MODEL, max_tokens=2048,
            system=SYSTEM, tools=TOOLS, messages=messages
        ) as stream:
            for event in stream:
                if event.type == "content_block_delta":
                    if event.delta.type == "text_delta":
                        print(event.delta.text, end="", flush=True)
            final = stream.get_final_message()

        messages.append({"role": "assistant", "content": final.content})
        if final.stop_reason == "end_turn":
            return

        tool_results = []
        for b in final.content:
            if b.type == "tool_use":
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": b.id,
                    "content": safe_run(b.name, b.input)
                })
        messages.append({"role": "user", "content": tool_results})
```

流式的好处：用户**立刻看到模型在打字**，体验差 100 倍。

---

## 七、第 6 版：历史压缩

当 `messages` 很长（> 100k token），模型会变慢、变贵。压缩思路：

```python
def compress_if_long(messages, threshold=80_000):
    # 简单做法：用 client.messages.count_tokens 估算
    tokens = client.messages.count_tokens(
        model=MODEL, messages=messages
    ).input_tokens
    if tokens < threshold:
        return messages

    # 取早期前 80% 摘要 + 最后 20% 保留
    cut = int(len(messages) * 0.8)
    early, recent = messages[:cut], messages[cut:]

    summary = client.messages.create(
        model=MODEL, max_tokens=2048,
        messages=[{"role": "user",
                   "content": f"用 500 字总结以下对话历史：\n{early}"}]
    ).content[0].text

    return [{"role": "user",
             "content": f"[历史摘要]\n{summary}"}] + recent
```

> Claude Code 用的是更复杂的"分段摘要 + 关键信息保留"。

---

## 八、第 7 版：人工审批 hook

危险操作（删文件、付款、发邮件）必须问人：

```python
DANGEROUS = {"delete_file", "send_email", "run_shell"}

def maybe_ask_human(name, args):
    if name in DANGEROUS:
        print(f"\n[审批] Agent 要执行: {name}({args})")
        ans = input("批准吗 (y/N): ").strip().lower()
        if ans != "y":
            return "USER_REJECTED: 用户拒绝执行"
    return None  # 没拦截

def safe_run(name, args, retries=2):
    rejection = maybe_ask_human(name, args)
    if rejection:
        return rejection
    # ... 后续重试逻辑
```

---

## 九、第 8 版：可观测性（trace）

```python
import json, time, pathlib

class Trace:
    def __init__(self, path="trace.jsonl"):
        self.path = pathlib.Path(path)
    def log(self, kind, payload):
        self.path.open("a").write(json.dumps({
            "t": time.time(), "kind": kind, "data": payload
        }, default=str) + "\n")

trace = Trace()

# 在主循环每一步记录
trace.log("step_start", {"messages_len": len(messages)})
trace.log("llm_response", {"stop_reason": r.stop_reason,
                           "usage": r.usage.model_dump()})
trace.log("tool_call", {"name": b.name, "input": b.input,
                        "result_preview": result[:200]})
```

事后就能复现 Agent 的每一步。

---

## 十、第 9 版：成本控制

```python
class Budget:
    def __init__(self, max_steps=20, max_cost_usd=1.0):
        self.steps, self.cost = 0, 0.0
        self.max_steps, self.max_cost = max_steps, max_cost_usd

    def add(self, usage):
        self.steps += 1
        # Sonnet 4.5 价格：$3/M input, $15/M output（示例）
        self.cost += (usage.input_tokens * 3 + usage.output_tokens * 15) / 1_000_000
        if self.steps >= self.max_steps:
            raise RuntimeError(f"超步数限制 {self.max_steps}")
        if self.cost >= self.max_cost:
            raise RuntimeError(f"超预算 ${self.max_cost:.2f}")
```

每次 LLM 返回后 `budget.add(r.usage)`。

---

## 十一、第 10 版：多步规划

让 Agent 先列计划再执行：

```python
PLAN_PROMPT = """
在执行任何工具之前，先用 1-5 步描述你的计划。
格式：
PLAN:
1. ...
2. ...
然后再开始动手。
"""
SYSTEM = SYSTEM + "\n" + PLAN_PROMPT
```

或更结构化：先调一个 `make_plan` 工具产出 JSON 计划，再逐步执行。

---

## 十二、整合：把 10 版拼成 mini-agent.py（约 300 行）

文件结构：

```
mini_agent/
  __init__.py
  agent.py        # 主循环
  tools.py        # 工具集（calculator, read_file, write_file, shell, search）
  budget.py       # 成本控制
  trace.py        # 可观测
  compress.py     # 历史压缩
  approve.py      # 人工审批
  cli.py          # 命令行入口
```

`agent.py` 主类（精简示意）：

```python
class MiniAgent:
    def __init__(self, system, tools, budget=None,
                 trace=None, dangerous=set(), max_steps=20):
        self.client = Anthropic()
        self.system = system
        self.tools = tools
        self.budget = budget or Budget(max_steps=max_steps)
        self.trace = trace or Trace()
        self.dangerous = dangerous
        self.messages = []

    def run(self, user_msg):
        self.messages.append({"role": "user", "content": user_msg})
        while True:
            self.messages = compress_if_long(self.messages)
            r = self.client.messages.create(
                model=MODEL, max_tokens=2048,
                system=self.system, tools=self.tools,
                messages=self.messages
            )
            self.budget.add(r.usage)
            self.trace.log("llm", {"stop": r.stop_reason})
            self.messages.append({"role": "assistant", "content": r.content})

            if r.stop_reason == "end_turn":
                return "".join(b.text for b in r.content if b.type == "text")

            tool_results = []
            for b in r.content:
                if b.type == "tool_use":
                    if b.name in self.dangerous:
                        if not approve(b.name, b.input):
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": b.id,
                                "content": "USER_REJECTED"
                            })
                            continue
                    try:
                        out = run_tool(b.name, b.input)
                    except Exception as e:
                        out = f"ERROR: {e}"
                    self.trace.log("tool", {"name": b.name, "out": out[:200]})
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": b.id,
                        "content": out
                    })
            self.messages.append({"role": "user", "content": tool_results})
```

---

## 十三、用 mini-agent 完成 5 个真实任务

写一份 `examples/run_tasks.py`：

1. **写文件**：让 Agent 写一首诗保存到 `out/poem.txt`
2. **跑命令**：让 Agent `ls -la` 当前目录并总结
3. **搜索**：接 Brave Search API 工具，让 Agent 查"2026 年最佳本地模型"
4. **计算**：复杂数学应用题
5. **总结**：让 Agent 读 README.md 并输出 3 行摘要

每个任务后看 `trace.jsonl`，能完整复现每一步。

---

## 十四、开源到 GitHub

把 `mini_agent/` 推到 GitHub，README 写：
- 它是什么
- 为什么 300 行
- 怎么用
- 与 LangGraph / OpenAI Agents SDK 对比

> 这会成为你简历里**很硬的一个项目**——会有面试官问你"主循环里 stop_reason 有几种"。

---

## 十五、✅ 本周 Checklist

- [ ] 第 1 版能跑（calculator）
- [ ] 第 2 版多工具 + 并行调用
- [ ] system prompt 改写后行为变化能感受到
- [ ] 流式输出顺畅
- [ ] 历史压缩在长对话里触发过一次
- [ ] 危险操作弹出审批
- [ ] trace.jsonl 能完整复盘一次跑
- [ ] budget 超了能正常熔断
- [ ] 5 个真实任务全部跑通
- [ ] 仓库 push 到 GitHub
- [ ] 工具抛异常时 Agent 能自己换策略，而不是整个循环崩掉
- [ ] 上下文压缩真实触发过一次，且摘要没丢掉关键约束
- [ ] trace 里能查到每次工具调用的入参、出参与耗时

---

## 十六、🐛 常见错误

| 错误现象 | 原因 | 解决 |
|---|---|---|
| `tool_use` 一直接收，循环停不下来 | 只判断了 `stop_reason == "end_turn"`，没处理 `tool_use` 分支 | 先判 `stop_reason`；是 `tool_use` 就执行工具、把结果回填后继续下一轮 |
| 报 `tool_result blocks must be in user message` | 把工具结果当成 assistant 消息发了回去 | Anthropic API 要求 tool_result 放在 **user** 消息里，且 `tool_use_id` 必须与请求一一对应 |
| 工具抛异常，Agent 直接崩 | 没有 try / except | 工具失败要 catch，把错误信息当 tool_result 回给模型，让它自己换策略 |
| 长对话超出上下文 | messages 无限追加 | 到阈值就压缩历史：保留 system + 最近 N 轮 + 摘要（§七） |
| 流式输出时 JSON 解析失败 | 按 chunk 拼 JSON | 流式里用增量解析或先聚合再解析；用 Claude Agent SDK 直接取 `final_message()` |
| 审批 hook 写在工具函数内部 | 审批散落在每个工具里，必然漏 | 统一在工具注册/执行入口做审批，一处管全部 |
| token 花费完全不可控 | 没有预算 | 每轮记 usage，超 max_steps / max_cost 立即停（§十） |

---

## 十七、📚 参考与延伸阅读

- Anthropic API 文档 · Tool use：<https://docs.anthropic.com/en/docs/agents-and-tools/tool-use>
- Anthropic API 文档 · Streaming：<https://docs.anthropic.com/en/api/messages-streaming>
- Anthropic Cookbook · `tool_use` 章（含多工具并行示例）：<https://github.com/anthropics/anthropic-cookbook>
- `anthropics/claude-agent-sdk-python` —— 工业级主循环、权限与 hook 的参考实现：<https://github.com/anthropics/claude-agent-sdk-python>
- 本路线第 01 篇（5 模式）、第 05 篇（给 mini-agent 接 MCP）

**手写完了再看 LangGraph，你会发现"哦，原来它就是把这些抽象成了图"。** 这正是下一周的内容。
