---
title: 类型系统与 Pydantic
type: weekly-tutorial
chapter: "01"
chapter_title: Python 从零到源码
order: 9
week: 8
duration: 7 天
daily_hours: 1.5
difficulty: ⭐⭐⭐⭐
prerequisites:
  - 第 03~04 篇
goals:
  - 让你的代码"自带说明书"。读 100 行别人的代码，从看 5 分钟变看 30 秒；从"运行时炸了"变"写代码时 IDE 就标红"；学会用 **Pydantic** 优雅地校验输入数据。
outputs:
  - 类型化重构
tags: [python, 类型注解, typing, mypy, pydantic, 工程化]
prev: "[[07-并发与异步]]"
next: "[[09-工程化与发布]]"
created: 2026-06-19
updated: 2026-11-25
---

# 第 08 篇 · 类型系统与 Pydantic 📐

> 本周目标：让你的代码"自带说明书"。读 100 行别人的代码，从看 5 分钟变看 30 秒；从"运行时炸了"变"写代码时 IDE 就标红"；学会用 **Pydantic** 优雅地校验输入数据。

---

## 1. 为什么需要类型注解？📜

**类比**：写代码 = 签合同。
- 没注解：合同上写"甲方给乙方东西"——给啥？什么时候？数量？全凭口头约定，扯皮起步。
- 有注解：合同上写"甲方在 2026/06/19 前给乙方 100 个苹果"——一目了然。

```python
# 没注解（传错了运行时才炸）
def add(a, b):
    return a + b

add("1", 2)        # 运行时 TypeError

# 有注解（IDE / mypy 提前告诉你错了）
def add(a: int, b: int) -> int:
    return a + b
```

> 💡 **划重点**：Python 是**动态类型**语言，注解**不会在运行时检查**（除非你用 Pydantic / typeguard）。它是给**人和工具**看的。

---

## 2. 基础类型注解 🧱

```python
name: str = "Alice"
age: int = 18
height: float = 1.75
is_student: bool = True

scores: list[int] = [90, 80, 70]                 # Python 3.9+ 直接用内置类型
profile: dict[str, str | int] = {"name": "A", "age": 18}
point: tuple[float, float] = (1.0, 2.0)

def greet(name: str, times: int = 1) -> None:
    for _ in range(times):
        print(f"hi {name}")
```

> ⚠️ Python 3.8 及之前要 `from typing import List, Dict, Tuple`，写 `List[int]`。3.9+ 推荐用小写内置 `list[int]`。**本教程默认 3.10+**。

---

## 3. typing 模块进阶 🛠️

| 注解                           | 含义                         | 例子                         |
| ---------------------------- | -------------------------- | -------------------------- |
| `Optional[X]` 或 `X \| None`  | X 或 None                   | `name: str \| None = None` |
| `Union[A, B]` 或 `A \| B`     | A 或 B                      | `x: int \| str`            |
| `Literal["a", "b"]`          | 只能是这几个具体值                  | `mode: Literal["r", "w"]`  |
| `Any`                        | 任何类型（关掉检查）                 | `data: Any`                |
| `Callable[[int, str], bool]` | 一个吃 (int, str) 返回 bool 的函数 | 见下                         |
| `Final[int]`                 | 常量，不能再赋值                   | `PI: Final = 3.14`         |

```python
from typing import Literal, Callable

def open_file(path: str, mode: Literal["r", "w", "a"] = "r") -> None:
    print(path, mode)

open_file("a.txt", "x")    # mypy 报错：Literal 只允许 r/w/a

def apply(fn: Callable[[int], int], x: int) -> int:
    return fn(x)

print(apply(lambda n: n * 2, 5))      # 10
```

### 🎯 动手练习 8.1
写一个 `parse_age(value: str | int) -> int`，传字符串和整数都能解析，非数字字符串抛 `ValueError`。

<details>
<summary>👀 参考答案</summary>

```python
def parse_age(value: str | int) -> int:
    if isinstance(value, int):
        return value
    if value.isdigit():
        return int(value)
    raise ValueError(f"非法年龄：{value!r}")

print(parse_age(18), parse_age("20"))     # 18 20
```
</details>

---

## 4. 泛型 TypeVar：给容器一个"占位符" 📦

如果你写了一个"装任何类型的栈"，你不希望写两次（一次给 int 一次给 str）：

```python
from typing import TypeVar, Generic

# T 是「类型占位符」—— 它本身不是类型，是「某个类型」的代号。
# 同一个类里所有 T 都指向「同一个具体类型」，由使用方在 Stack[int] 时确定。
# 注意：TypeVar 只在类型检查器里起作用，运行时它就是个普通对象。
T = TypeVar("T")

class Stack(Generic[T]):
    # Generic[T] 声明：Stack 是泛型类，T 是它的「类型参数」。
    # 不继承 Generic[T] 的话，mypy 会把 T 当成未定义，Stack[int] 也不合法。

    def __init__(self) -> None:
        # list[T] 是「元素类型为 T 的列表」—— 只在注解里用，不影响运行时。
        # Python 3.9+ 可直接写 list[T]；3.8 及以下要写 List[T]（从 typing import List）。
        self._items: list[T] = []

    def push(self, x: T) -> None:
        # 参数 x 是 T —— 当 Stack[int] 时，这里等价于 push(self, x: int)。
        self._items.append(x)

    def pop(self) -> T:
        # 返回 T —— Stack[int].pop() 的静态返回类型是 int。
        # ⚠️ 空栈时这行抛 IndexError，类型系统管不到运行时的空栈。
        return self._items.pop()

s: Stack[int] = Stack()
# 右边 Stack() 不带参数，mypy 会根据左边的注解推断成 Stack[int]。
# 也可以显式写 Stack[int]() —— 但运行时两者完全一样，见下文第 1 条。

s.push(1)
s.push("oops")     # mypy 报错：期望 int，得到 str
```

---

## 5. Protocol：结构化类型 = 鸭子类型 + 检查 🦆

**类比**：你不在乎它**叫什么名字**（class），只在乎它**会不会嘎嘎叫**（方法）。

```python
from typing import Protocol

class Drawable(Protocol):
    # Protocol 定义的是「接口契约」，不是「基类」。
    # 方法体写 ... —— 这里永远不执行，只是声明签名。
    # 关键：Circle 和 Square 不继承 Drawable，也不需要「注册」。
    # 只要它们「有 draw(self) -> None」，mypy 就认为它们满足 Drawable。
    def draw(self) -> None: ...

class Circle:
    def draw(self) -> None:
        print("画圆")

class Square:
    def draw(self) -> None:
        print("画方")

def render(items: list[Drawable]) -> None:
    # items 的静态类型是 list[Drawable]。
    # mypy 会检查「传进来的 list 的元素类型」是否满足 Drawable：
    #   list[Circle]  → Circle 有 draw() -> None → ✅
    #   list[Square]  → Square 有 draw() -> None → ✅
    # 但注意：运行时 render 里对 items 没有任何类型检查，it.draw() 就是普通属性访问。
    for it in items:
        it.draw()

render([Circle(), Square()])     # ✅ 它们都没继承 Drawable，但都"长得像"
```

> 💡 Protocol 是 Python 类型系统里最优雅的设计之一，比 Java 的 interface 灵活。

---

## 6. TypedDict：给字典加结构 📋

```python
from typing import TypedDict


class User(TypedDict):
    # 类体里只写「键: 类型」，没有 __init__、没有方法、没有默认值。
    # 默认 total=True —— 所有键都是「必需的」。
    id: int
    name: str
    email: str


u: User = {"id": 1, "name": "Alice", "email": "a@x.com"}    # ✅
# ⚠️ 运行时 u 就是一个普通 dict —— type(u) 是 dict，不是 User。
#    TypedDict 只在 mypy/pyright 眼里存在，运行时完全消失。

bad: User = {"id": "1"}                                       # mypy 报错
# 这里其实有两个错误：
#   1. 缺了 name 和 email（total=True 时必需）
#   2. id 是 str 不是 int
# mypy 通常只报第一个，修完再报第二个 —— 别以为只有一个问题。
```

适合处理 JSON / API 响应。

---

## 7. 类型别名：给复杂类型起小名 🏷️

```python
type UserId = int                       # Python 3.12+ 新语法
type Vector = list[float]
type JSON = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None

def add_one(uid: UserId) -> UserId:
    return uid + 1
```

---

## 8. mypy：静态类型检查 🔍

安装：

```bash
pip install mypy
mypy your_file.py
```

例子：

```python
# bad.py
def add(a: int, b: int) -> int:
    return a + b

print(add("1", 2))
```

```bash
$ mypy bad.py
bad.py:4: error: Argument 1 to "add" has incompatible type "str"; expected "int"
Found 1 error in 1 file
```

常用配置 `pyproject.toml`：

```toml
[tool.mypy]
python_version = "3.13"
strict = true                  # 全部最严格
disallow_untyped_defs = true   # 函数必须写注解
```

---

## 9. ruff：超快的代码风格 + 类型检查工具 ⚡

ruff 用 Rust 写，比 flake8 / black / isort 快 10-100 倍。**一个工具替代三个**。

```bash
pip install ruff
ruff check .          # 静态检查
ruff format .         # 自动格式化
```

`pyproject.toml`：

```toml
[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]  # 错误/未用/import 排序/升级语法/bugbear/简化
```

> 💡 推荐 VSCode 装 "Ruff" 插件，保存自动格式化。

---

## 10. Pydantic v2：数据校验之王 🛡️

类比：dataclass 是"自动写 `__init__` 的傻瓜模式"，Pydantic 是"dataclass + 在运行时检查类型 + 自动转换 + 错误信息漂亮"。

安装：

```bash
pip install pydantic
```

```python
from pydantic import BaseModel, Field, EmailStr, field_validator

class User(BaseModel):
    # 字段声明 = 类型 + 约束。pydantic 在「实例化时」运行校验，
    # 不通过直接抛 ValidationError —— 这是它和 dataclass / TypedDict 的根本区别。

    id: int
    # 只写类型，没有额外约束。默认「宽松模式」：传 "1" 会尝试转成 1。

    name: str = Field(min_length=1, max_length=20)
    # Field 的参数是「校验规则」，不是普通默认值。
    # min_length / max_length 在「类型校验之后」检查 —— 见第 3 条。

    age: int = Field(ge=0, le=150)        # ge=大于等于, le=小于等于
    # ge / le 是数值约束，等价于 0 <= age <= 150。
    # 还有 gt / lt（严格大于/小于）。

    email: EmailStr                        # 自动校验邮箱格式
    # EmailStr 依赖 email-validator 包：pip install "pydantic[email]"
    # 没装的话 import 时报错，不是运行到 email 字段才报。

    tags: list[str] = []
    # ⚠️ 这里和 dataclass 的关键区别：
    #    dataclass 里写 `tags: list = []` 会报 "mutable default" 错误；
    #    pydantic 会自动把默认值「深拷贝」到每个实例 —— 不会出现「所有实例共享同一个 list」的坑。
    #    这是 pydantic 相对 dataclass 的便利之一。

    @field_validator("name")
    @classmethod
    def name_no_space(cls, v: str) -> str:
        # 自定义校验器：在「类型校验通过之后」执行。
        # 所以这里的 v 一定是 str，不用再判断类型。
        # 抛 ValueError → pydantic 捕获并包装成 ValidationError 的一条错误。
        if " " in v:
            raise ValueError("name 不能含空格")
        return v.strip()
        # ⚠️ 校验器返回的值会「替换」原值 —— 所以 strip 后的结果才是最终存进模型的。
        # 但检查空格在 strip 之前，顺序是有意的：`" A "` 会被 strip 成 `"A"` 通过，
        # `"A B"` 因为含空格被拒。如果先 strip 再查，`" A B "` 也会被拒 —— 行为不同。

# 字符串自动转 int
u = User(id="1", name="Alice", age=18, email="a@x.com")
print(u)
# 输出：id=1 name='Alice' age=18 email='a@x.com' tags=[]
# ⚠️ id 已经是 int 1，不是字符串 "1" —— 转换发生在校验时。

# 校验失败
try:
    User(id="x", name="A B", age=-1, email="not-an-email")
except Exception as e:
    print(e)
# ⚠️ pydantic 会「收集所有错误」再抛，不是遇到第一个就停。
# 这个例子里 4 个字段都错，ValidationError 里会有 4 条错误信息。
# 用 except ValidationError 更精确，但当前 except Exception 也能接住。
```

**运行结果**：
```
id=1 name='Alice' age=18 email='a@x.com' tags=[]
4 validation errors for User
id
  Input should be a valid integer ...
name
  Value error, name 不能含空格 ...
age
  Input should be greater than or equal to 0 ...
email
  value is not a valid email address ...
```

### 序列化：model_dump / model_dump_json

```python
print(u.model_dump())              # 转 dict
# v2 的 API（v1 是 .dict()）。
# 返回的是「纯 Python dict」——嵌套的 BaseModel 也会递归转成 dict。
# ⚠️ 但 datetime / Path / Enum 等对象「仍是原对象」，不是字符串

print(u.model_dump_json(indent=2)) # 转 JSON
# v2 的 API（v1 是 .json()）。
# 返回 JSON 字符串：datetime 自动转 ISO 8601、Enum 自动转 value、
# 中文默认原样输出（ensure_ascii=False）。
```

### 反序列化

```python
data = '{"id": 2, "name": "Bob", "age": 30, "email": "b@x.com"}'
u2 = User.model_validate_json(data)
# v2 的 API（v1 是 .parse_raw()）。
# 一步完成：解析 JSON 字符串 → 按 User 的规则校验 → 返回 User 实例。
# 缺字段时用默认值，多字段默认忽略（见第 5 条），类型不合法抛 ValidationError。

print(u2)
```

---

## 11. 实战：用 Pydantic 重构第 03 篇的 cli-todo 🎯

第 03 篇的 todo 是一个 list of dict，没校验，乱传值会出各种问题。我们用 Pydantic 重写：

```python
# todo.py —— 第 03 篇 cli-todo 的 Pydantic 重写版
# 用法（和第 03 篇完全一致）：
#   python todo.py add "写代码"
#   python todo.py list
#   python todo.py done 1
#   python todo.py remove 2
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from pathlib import Path
from typing import Literal
import sys

# ── 异常体系：兑现第 03 篇的承诺 —— 不再裸抛 ValueError，定义自己的分层 ──
class TodoError(Exception):
    """本工具所有错误的基类。调用方 except TodoError 就能接住全部业务错误。"""

class TaskNotFound(TodoError, ValueError):
    """任务不存在。

    同时继承 TodoError 和 ValueError 是有意为之：
    - 老代码写 except ValueError 的，照样能接住（向后兼容，不破坏第 03 篇的 main）；
    - 新代码可以 except TaskNotFound 精确处理。
    成熟库（requests、sqlalchemy）都这么设计异常树 —— 这就是"异常体系"的样子。
    """

class Task(BaseModel):
    id: int
    title: str = Field(min_length=1, max_length=80)
    status: Literal["todo", "doing", "done"] = "todo"
    # default_factory 而不是 default=datetime.now()：
    # 后者在「类定义时」求值一次，所有实例共享同一个时间。
    # 前者每次实例化才调用，每个 Task 拿到独立的时间戳。
    # 这是 dataclass 和 pydantic 共有的经典坑。
    created_at: datetime = Field(default_factory=datetime.now)

class TaskList(BaseModel):
    # list[Task] 是「嵌套模型」—— 传进来 dict 会自动转成 Task 实例，
    # 这是 pydantic 的核心能力：递归校验嵌套结构。
    # 默认值 [] 在 pydantic 里会被深拷贝，每个 TaskList 拿到独立 list。
    tasks: list[Task] = []

    def add(self, title: str) -> Task:
        # max(..., default=0) + 1：空列表时第一个 id 是 1。
        # ⚠️ 现在 remove 有了：删掉尾部任务再加，会复用旧 id。
        #    彻底避免要维护 next_id 字段 —— 见练习 8.3。
        # ⚠️ 并发调用 add 会撞 id（max 和 append 之间有间隙）—— 单线程无所谓。
        new_id = max((t.id for t in self.tasks), default=0) + 1
        t = Task(id=new_id, title=title)
        self.tasks.append(t)
        return t

    def list(self) -> list[Task]:
        # 对应第 03 篇的 cmd_list：返回模型列表，格式化交给调用方 —— 数据与展示分离。
        return self.tasks

    def done(self, tid: int) -> None:
        # 遍历 O(n)。任务量小无所谓；上千个任务应改成 dict 索引。
        for t in self.tasks:
            if t.id == tid:
                # ⚠️ pydantic v2 默认 validate_assignment=False ——
                # 这里赋值「不会」重新校验。当前值是合法的 "done"，所以没事；
                # 但 t.status = "invalid" 也不会报错，直到下次序列化/反序列化才炸。
                t.status = "done"
                return
        raise TaskNotFound(f"任务不存在 id={tid}")
        # ⚠️ 类型注解 int 不做运行时检查：done("1") 不会 TypeError，
        #    只会因为 "1" != 1 走到这里抛 TaskNotFound。
        #    想拦住非法类型要么显式 isinstance，要么交给 CLI 层 int() 转换。

    def remove(self, tid: int) -> None:
        # 对应第 03 篇的 cmd_remove：用新列表重建，不能在遍历时删原列表。
        remaining = [t for t in self.tasks if t.id != tid]
        if len(remaining) == len(self.tasks):
            raise TaskNotFound(f"任务不存在 id={tid}")
        self.tasks = remaining

    def save(self, path: Path) -> None:
        # model_dump_json 是 v2 的 API（v1 是 .json()）。
        # 默认 ensure_ascii=False —— 中文「写第 08 篇教程」直接原样写入，不转 \uXXXX。
        # ⚠️ 没有原子写 —— 写到一半崩溃会损坏原文件。生产环境用 safe_writer（第 05 篇）。
        path.write_text(self.model_dump_json(indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "TaskList":
        # 返回类型写 "TaskList"（字符串）而不是 TaskList：
        # 类体里还没定义完这个类，直接写名字会 NameError。
        # 这是「前向引用」，pydantic 和普通类都需要。
        if not path.exists():
            return cls()                # 首次运行，没有文件 → 空列表
        # ⚠️ 文件存在但 JSON 损坏 / 字段不合法时，这里会抛
        #    ValidationError（或 json 层的 JSONDecodeError），程序直接崩。
        #    生产环境应 catch 后备份坏文件、返回空 TaskList。
        return cls.model_validate_json(path.read_text(encoding="utf-8"))

# ── CLI 层：和第 03 篇一样的四个命令，异常处理换成接 TaskNotFound ──
def main(argv: list[str]) -> int:
    db = Path("todos.json")             # 文件名沿用第 03 篇；⚠️ 但顶层结构从「数组」
    # 升级成了 {"tasks": [...]}，旧文件直接 load 会抛 ValidationError。
    # 迁移很简单：json.loads 读出旧 list → TaskList(tasks=旧列表) → save 一次即可。
    if len(argv) < 2:
        print("用法：python todo.py <add|list|done|remove> [参数]")
        return 1
    action = argv[1]
    try:
        tl = TaskList.load(db)
        if action == "add":
            t = tl.add(argv[2])
            tl.save(db)
            print(f"已添加 #{t.id}: {t.title}")
        elif action == "list":
            tasks = tl.list()
            if not tasks:
                print("还没有任务，先用 add 加一条")
            for t in tasks:
                mark = "x" if t.status == "done" else " "
                print(f"[{mark}] {t.id}. {t.title}")
        elif action == "done":
            tl.done(int(argv[2]))       # int() 转换失败抛 ValueError，下面统一接
            tl.save(db)
            print(f"已完成 #{argv[2]}")
        elif action == "remove":
            tl.remove(int(argv[2]))
            tl.save(db)
            print(f"已删除 #{argv[2]}")
        else:
            print(f"未知命令：{action}")
            return 1
    except TaskNotFound as e:
        print(e)
        return 1
    except ValidationError as e:
        # Pydantic 校验错误兜底：空标题、超长标题等都会走到这。
        print(f"数据校验失败：{e.errors()[0]['msg']}")
        return 1
    except (ValueError, IndexError):
        print("参数不对：done/remove 需要一个数字 id，add 需要一个标题")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

**运行示例**：

```
$ python todo.py add "写第 08 篇教程"
已添加 #1: 写第 08 篇教程
$ python todo.py add "学 Pydantic"
已添加 #2: 学 Pydantic
$ python todo.py done 1
已完成 #1
$ python todo.py list
[x] 1. 写第 08 篇教程
[ ] 2. 学 Pydantic
$ python todo.py done 99
任务不存在 id=99
```

数据文件 `todos.json`（沿用第 03 篇的文件名，结构升级为嵌套模型）：
```json
{
  "tasks": [
    {"id": 1, "title": "写第 08 篇教程", "status": "done", "created_at": "..."},
    {"id": 2, "title": "学 Pydantic", "status": "todo", "created_at": "..."}
  ]
}
```

> 💡 **对照第 03 篇，这次重写升级了什么**（T8 的完整答案）：
> 1. `list[dict]` → `TaskList` 嵌套模型：字段有类型、有约束（title 长度、status 只能是三个值），脏数据在 add 当场被拒，而不是写进文件下次读才炸；
> 2. 裸 `ValueError` → `TodoError`/`TaskNotFound` 异常体系，调用方能精确捕获（同时兼容 `except ValueError` 的老写法）；
> 3. 第 03 篇的 **add / list / done / remove 四个命令全部保留** —— 重写不是阉割，功能必须对齐 T3。

### 🎯 动手练习 8.2
给 `Task` 增加字段 `priority: Literal["low", "mid", "high"] = "mid"` 和 `due: datetime | None = None`，并加一个校验器：截止时间不能早于创建时间。

<details>
<summary>👀 参考答案</summary>

```python
from pydantic import model_validator

class Task(BaseModel):
    id: int
    title: str
    priority: Literal["low", "mid", "high"] = "mid"
    due: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.now)

    @model_validator(mode="after")
    def check_due(self):
        if self.due and self.due < self.created_at:
            raise ValueError("due 不能早于 created_at")
        return self
```
</details>

### 🎯 动手练习 8.3
正文 `add` 的注释提到：删掉尾部任务后再 add 会**复用旧 id**。给 `TaskList` 加一个 `next_id: int = 1` 字段，`add` 用它分配 id 并递增，让 id 永不复用。想想：为什么 `next_id` 要存进文件而不是每次 `max()+1` 现算？

<details>
<summary>👀 参考答案</summary>

```python
class TaskList(BaseModel):
    tasks: list[Task] = []
    next_id: int = 1          # 持久化的"发号器"，随 save 一起写进 JSON

    def add(self, title: str) -> Task:
        t = Task(id=self.next_id, title=title)
        self.next_id += 1     # 发号后立刻递增，删除任务不影响它
        self.tasks.append(t)
        return t
```

为什么存文件：`max()+1` 是**从现存数据反推**，删掉最大 id 后计数器就"退回"了，新任务会复用旧 id —— 如果别处（日志、外键、分享链接）还引用着旧 id，数据就串了。`next_id` 是**单调发号器**，状态独立于数据本身，这正是数据库自增序列的原理。
</details>


---

## ✅ 本周检查清单

- [ ] 能给函数参数和返回值加正确的类型注解
- [ ] 知道 `Optional[X]` = `X | None`
- [ ] 用过 `Literal` 限定字符串取值
- [ ] 写过一个用 `TypeVar` 的泛型类
- [ ] 写过一个 `Protocol` 接口
- [ ] 在项目里跑过 mypy 和 ruff
- [ ] 用 Pydantic 写过一个 `BaseModel` 并触发过校验错误
- [ ] 把第 03 篇的 cli-todo 用 Pydantic 重构了（**add/list/done/remove 四个命令都在**，并定义了 `TodoError`/`TaskNotFound` 异常体系）

## 🐛 常见错误集合

| 错误 | 原因 | 解决 |
|------|------|------|
| `name 'list' is not subscriptable` | Python < 3.9 | 用 `from __future__ import annotations` 或 `from typing import List` |
| `Optional[int]` 还能传 None | 注解只是给工具看 | 用 mypy 检查 / Pydantic 运行时校验 |
| Pydantic v1 用法在 v2 报错 | API 大改 | 看官方迁移指南：v1 `dict()` → v2 `model_dump()` |
| `EmailStr` ImportError | 没装 | `pip install "pydantic[email]"` |
| mypy 太严格、报老代码错 | 一开始就 strict | 渐进开严：先 `disallow_untyped_defs`，再加其他 |

## 📚 延伸阅读

- 官方 typing：https://docs.python.org/zh-cn/3/library/typing.html
- mypy 官方文档：https://mypy.readthedocs.io/
- Pydantic v2 文档：https://docs.pydantic.dev/
- ruff 文档：https://docs.astral.sh/ruff/
- PEP 484（类型注解）：https://peps.python.org/pep-0484/
- PEP 544（Protocol）：https://peps.python.org/pep-0544/

> 🎉 学完本章，你的代码已经"自带说明书"。下周我们把它**打包发布到 PyPI**，让全世界 `pip install` 你的工具。
