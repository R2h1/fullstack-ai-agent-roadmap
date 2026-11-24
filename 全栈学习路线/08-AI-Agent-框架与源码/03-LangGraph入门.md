---
title: LangGraph 入门
type: weekly-tutorial
chapter: "08"
chapter_title: AI Agent 框架与源码
order: 4
week: 3
estimated_hours: 16
difficulty: ⭐⭐⭐⭐
prerequisites:
  - 第 02 篇
outputs:
  - LangGraph 基础
tags: [langgraph, langchain, state-machine, agent-framework]
prev: "[[02-手写Agent不用框架]]"
next: "[[04-LangGraph进阶]]"
created: 2026-06-19
updated: 2026-11-23
---

# 第 03 篇 · LangGraph 入门

> 上一周你手写了 mini-agent，知道**循环**长什么样。这一周用 LangGraph 把"循环"变成"图"。

---

## 一、LangChain vs LangGraph：什么关系？

| | LangChain | LangGraph |
|---|---|---|
| 定位 | LLM 调用链工具箱 | 状态机式 Agent 框架 |
| 抽象 | Chain / Runnable | Graph / Node / Edge |
| 适合 | 简单顺序流 | 循环、分支、多 Agent |
| 现状 | 老牌、API 偏冗杂 | LangChain 团队 2024 主推、事实标准 |

**结论：写 Agent 直接用 LangGraph，不用纠结 LangChain。**

---

## 二、为什么大家都选 LangGraph？

1. **状态机心智模型**：和真实 Agent 工作方式一致。
2. **持久化（Checkpointer）**：内建 SQLite/Postgres 存档，断点恢复。
3. **Human-in-the-loop**：内建 `interrupt()`，比手写优雅。
4. **可视化（LangGraph Studio）**：图能在 IDE 里实时看见。
5. **生态大**：Anthropic / OpenAI / 各厂自家 Agent 也用它的运行时。
6. **部署（LangGraph Cloud / Server）**：写完直接上线。

类比：**LangGraph 是 Agent 界的 React**——不是必需品，但是事实标准。

---

## 三、安装

```bash
pip install langgraph langchain-anthropic langchain-core
export ANTHROPIC_API_KEY=...
```

---

## 四、Hello Graph（最小例子）

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    text: str

def upper(state: State) -> State:
    return {"text": state["text"].upper()}

graph = StateGraph(State)
graph.add_node("upper", upper)
graph.add_edge(START, "upper")
graph.add_edge("upper", END)

app = graph.compile()
print(app.invoke({"text": "hello"}))   # {'text': 'HELLO'}
```

恭喜，**你写了第一个 LangGraph**。

---

## 五、核心三概念

### 1. State（状态）

**整张图共享的字典**，每个节点读它、写它。

```python
class State(TypedDict):
    messages: list
    user_name: str
    step_count: int
```

### 2. Node（节点）

**普通 Python 函数**：吃 state，吐 state 的 *部分更新*。

```python
def my_node(state: State) -> dict:
    return {"step_count": state["step_count"] + 1}
```

返回的字典会**合并**进 state。

### 3. Edge（边）

- `add_edge(A, B)`：A 完成后必走 B
- `add_conditional_edges(A, fn)`：fn 看 state 决定下一步
- `START` / `END`：内置起止节点

---

## 六、6 步构建 StateGraph

```python
# 1. 定义 State
class State(TypedDict): ...

# 2. 创建 graph
graph = StateGraph(State)

# 3. 加节点
graph.add_node("plan", plan_fn)
graph.add_node("act", act_fn)

# 4. 加边
graph.add_edge(START, "plan")
graph.add_conditional_edges("plan", should_act,
                             {"yes": "act", "no": END})
graph.add_edge("act", "plan")  # 循环

# 5. 编译
app = graph.compile()

# 6. 调用
app.invoke({...})
# 或流式
for chunk in app.stream({...}):
    print(chunk)
```

---

## 七、实例 1：多节点顺序

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    topic: str
    outline: str
    article: str

def make_outline(s):
    return {"outline": f"## {s['topic']}\n1. 引言\n2. 主体\n3. 结论"}

def write_article(s):
    return {"article": f"基于大纲写文章：\n{s['outline']}\n（正文略）"}

g = StateGraph(State)
g.add_node("outline", make_outline)
g.add_node("write", write_article)
g.add_edge(START, "outline")
g.add_edge("outline", "write")
g.add_edge("write", END)
app = g.compile()

print(app.invoke({"topic": "LangGraph 入门"}))
```

---

## 八、实例 2：条件分支

```python
class State(TypedDict):
    msg: str
    label: str

def classify(s):
    if "退款" in s["msg"]: return {"label": "refund"}
    if "技术" in s["msg"]: return {"label": "tech"}
    return {"label": "faq"}

def refund(s): return {"msg": "已转给退款专员"}
def tech(s): return {"msg": "已转给技术专员"}
def faq(s): return {"msg": "FAQ: 请查官网"}

def route(s): return s["label"]   # 返回字符串决定走哪条

g = StateGraph(State)
g.add_node("classify", classify)
g.add_node("refund", refund); g.add_node("tech", tech); g.add_node("faq", faq)

g.add_edge(START, "classify")
g.add_conditional_edges("classify", route,
                         {"refund": "refund", "tech": "tech", "faq": "faq"})
for n in ["refund", "tech", "faq"]:
    g.add_edge(n, END)
app = g.compile()
print(app.invoke({"msg": "我要退款", "label": ""}))
```

---

## 九、实例 3：循环（条件边回到自己）

```python
class State(TypedDict):
    n: int
    log: list

def step(s):
    return {"n": s["n"] + 1, "log": s["log"] + [s["n"]]}

def cont(s):
    return "loop" if s["n"] < 5 else "done"

g = StateGraph(State)
g.add_node("step", step)
g.add_edge(START, "step")
g.add_conditional_edges("step", cont, {"loop": "step", "done": END})
app = g.compile()
print(app.invoke({"n": 0, "log": []}))
# {'n': 5, 'log': [0,1,2,3,4]}
```

---

## 十、Reducer：状态合并策略

默认 state 字段是**覆盖**。但有些字段（如 `messages`）你希望 **追加**。

```python
from typing import Annotated
from operator import add
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]   # 追加而不是覆盖
    counter: Annotated[int, add]              # 累加
    log: Annotated[list, add]                 # 列表拼接
```

`Annotated[T, reducer]` 告诉 LangGraph："这个字段更新时用 reducer 合并"。

`add_messages` 还会**自动按 id 去重**，是消息列表标配。

---

## 十一、ReAct Agent 模板

开箱即用的 ReAct Agent 现在由 **LangChain v1 的 `create_agent`** 提供：

> ⚠️ `langgraph.prebuilt.create_react_agent` 在 LangGraph v1 已弃用，请改用 `langchain.create_agent`（支持 middleware）。

```python
from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """查天气"""
    return f"{city} 24度晴"

import ast, math

# 只允许数字与四则运算，禁掉函数调用/属性访问/变量注入
_ALLOWED_NODES = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant,
                  ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod,
                  ast.Pow, ast.USub, ast.UAdd, ast.Load)

def _safe_eval(expr: str) -> float:
    tree = ast.parse(expr, mode="eval")
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"表达式包含不允许的语法: {type(node).__name__}")
    return eval(compile(tree, "<calc>", "eval"), {"__builtins__": {}}, math.__dict__)

@tool
def calc(expr: str) -> str:
    """计算（只支持四则运算）"""
    try:
        return str(_safe_eval(expr))
    except Exception as e:
        return f"计算失败: {e}"

llm = ChatAnthropic(model="claude-sonnet-5-5")
agent = create_agent(llm, tools=[get_weather, calc])

result = agent.invoke({"messages": [{"role": "user",
                                       "content": "北京天气如何？1+2 等于几？"}]})
for m in result["messages"]:
    print(m.type, ":", m.content)
```

**3 行配工具，Agent 就有了**。这是日常最常用的捷径。

> ⚠️ **别在生产里裸写 `eval(expr)`**。工具入参直接来自模型输出，等于把 `__import__`、`open` 全交出去了 —— 模型被诱导执行一次 `eval("__import__('os').system('rm -rf /')")` 就完蛋。上面的 `_safe_eval` 先用 `ast` 白名单把语法限死在四则运算，再关掉 `__builtins__`。真实项目里更推荐：① 换成 `sympy` / `simpleeval` 这类表达式求值库；② 或干脆不给模型"算任意表达式"的能力，只暴露 `add/mul/...` 这类固定工具。

---

## 十二、ToolNode：把工具列表变节点

如果你想**自己画图**而不是用 prebuilt：

```python
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, START, END

tools = [get_weather, calc]
tool_node = ToolNode(tools)

llm_with_tools = ChatAnthropic(model="claude-sonnet-5-5").bind_tools(tools)

def call_llm(state):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

def should_continue(state):
    last = state["messages"][-1]
    return "tools" if last.tool_calls else END

g = StateGraph(MessagesState)
g.add_node("llm", call_llm)
g.add_node("tools", tool_node)
g.add_edge(START, "llm")
g.add_conditional_edges("llm", should_continue, {"tools": "tools", END: END})
g.add_edge("tools", "llm")
agent = g.compile()
```

**这就是 ReAct 的内部实现**。看懂这张图，你就懂了 90% 的 LangGraph。

---

## 十三、本周实战：用 LangGraph 重写第 01 篇的 5 模式

写 5 个 .py 文件，每个一张图：

| 模式 | 图结构提示 |
|---|---|
| Prompt Chaining | `START → outline → write → polish → END` |
| Routing | `START → classify → 条件边 → faq/tech/refund → END` |
| Parallelization | START 后三条边并行到三个翻译节点，再汇合到 merge |
| Orchestrator-Workers | orchestrator 用 `Send` API 派 N 个 worker，再 reducer 汇合（第 04 篇详细讲）|
| Evaluator-Optimizer | `gen → eval`，eval 条件边：PASS→END，FAIL→gen |

跑通后对比第 01 篇纯 SDK 版本的代码量和清晰度。

---

## 十四、✅ 本周 Checklist

- [ ] Hello Graph 能跑
- [ ] 能讲清 State / Node / Edge
- [ ] 条件边、循环都写过
- [ ] 知道 reducer 怎么用，`add_messages` 用过
- [ ] `create_agent` 跑通
- [ ] 自己画的 ToolNode + LLM 图跑通
- [ ] 5 模式 LangGraph 版全部跑通
- [ ] 能解释 reducer 到底解决了什么问题（覆盖 vs 追加）
- [ ] 跑过一次 `recursion_limit` 触发，并知道怎么改
- [ ] 知道 `create_agent`（快捷）和自己画图各适合什么场景

---

## 十五、🐛 常见错误

| 错误现象 | 原因 | 解决 |
|---|---|---|
| `messages` 里只剩最后一条 | state 字段没有配 reducer，后写覆盖先写 | 用 `MessagesState`，或给字段加 `Annotated[list, add_messages]` |
| `add_conditional_edges` 报 key 不匹配 | 条件函数返回值不在映射字典里 | 返回值必须与映射的 key 完全一致（`"tools"` / `END`） |
| `RecursionError` / 死循环 | 条件边回到了自己却没有出口 | 补终止条件，并显式设 `app.invoke(..., {"recursion_limit": 25})` |
| 节点写了但没生效 | 节点函数返回了整个 state 或返回非 dict | 节点只返回**变化的键**：`return {"messages": [...]}` |
| state 类型报错 | 用了 dataclass / Pydantic 模型当 state | LangGraph v1 的 state 用 TypedDict（普通 dict）即可 |
| `create_agent` 传了 ToolNode 报错 | v1 的 `tools` 只接受工具列表 | `create_agent(llm, tools=[BaseTool...])`；ToolNode 只能自己 `add_node` |
| 工具结果对不上号 | 工具名或 tool_call id 拼错 | 用 `tools_by_name[call["name"]]`，回填时带上原始 `tool_call["id"]` |

---

## 十六、📚 参考与延伸阅读

- LangGraph 官方文档（v1）：<https://docs.langchain.com/oss/python/langgraph>
- LangChain v1 迁移指南（`create_react_agent` → `create_agent`、middleware）：<https://docs.langchain.com/oss/python/migrate/langchain-v1>
- LangGraph 源码 · `prebuilt/tool_node.py`、`graph/state.py`：<https://github.com/langchain-ai/langgraph>
- LangGraph 教程 · *Build a chatbot*
- 本路线第 02 篇（对照手写版）、第 04 篇（子图 / Send / Checkpointer）

下一周：**子图、Send、Checkpointer、人工审批、Streaming、Studio**——LangGraph 进阶全家桶。
