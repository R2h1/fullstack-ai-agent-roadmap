---
title: React 入门与 JSX
type: weekly-tutorial
chapter: "04"
chapter_title: React 从使用到源码
order: 2
week: 1
duration: 7 天
daily_hours: 2-3
difficulty: ⭐⭐
prerequisites: []
goals:
  - 建立「UI = f(state)」心智模型；能手写 JSX（懂五条铁律与 jsx/classic 两种编译产物）、函数组件、Props/children、条件与列表渲染（key 的意义）。
  - 周末交付：Todo（含过滤、原生拖拽排序）+ 计算器（连续计算状态机）——对应总纲第 01 篇产出与 T1 的前两件。
outputs:
  - 计算器 + Todo
tags: [react, jsx, vite, typescript, components, props]
prev: "[[00-React总纲]]"
next: "[[02-Hooks全集]]"
created: 2026-06-19
updated: 2026-11-28
---
 
# 第 01 篇 · React 入门与 JSX

## 0. 一句话理解 React

> React = "**用 JS 描述 UI**" 的库。

类比：以前写网页是「**手动操作 DOM**」——
拿到 div，改 textContent，再 appendChild 一个 button，再 addEventListener……像在工地搬砖。

React 是「**声明式 UI 模板引擎**」——
你只描述「**当数据是这样时，UI 应该长什么样**」，剩下的「**怎么把旧 UI 变成新 UI**」交给 React。

```js
// 命令式（旧）：你告诉浏览器一步一步怎么做
const div = document.createElement('div')
div.textContent = '点击次数: 0'
document.body.appendChild(div)

// 声明式（React）：你告诉 React UI 长什么样
function Counter() {
  const [n, setN] = useState(0)
  return <div onClick={() => setN(n + 1)}>点击次数: {n}</div>
}
```

记住这句：**UI = f(state)**。状态变了，UI 自动跟着变。

---

## 1. React 19 / Server Components 现状

到 2026 年，主流栈如下：

| 版本 | 关键特性 |
|---|---|
| React 18 (2022) | 并发渲染、Suspense、Automatic Batching（历史：React 19 已取代） |
| React 19 (2024) | `use()` Hook、Actions、Server Components 稳定、表单 hook |
| React Compiler (2024-2026) | 自动 memo，告别 useMemo/useCallback 滥用（2025-10 发布 v1.0 稳定版，需显式开启） |

**Server Components (RSC)**：组件可以"在服务端渲染、不发送 JS 到客户端"。本周不用，本章第 06 篇讲 Next.js 时再深入。

**并发渲染**：React 可以"暂停"一个慢渲染去做更紧急的事，让界面不卡。靠 `useTransition` / `useDeferredValue` 触发。

本周只学**客户端 React + 函数组件 + Hook**——这是 90% 项目的基础。

---

## 2. 创建项目（Vite + React 19 + TS）

```bash
pnpm create vite my-app --template react-ts
cd my-app
pnpm install
pnpm dev
```

打开 `http://localhost:5173`，看到旋转 logo 就成功了。

> 没有 pnpm？`npm i -g pnpm` 装一下。或者用 `npm create vite@latest`。

### 2.1 项目结构详解

```
my-app/
├── index.html          # 入口 HTML，<div id="root"></div>
├── vite.config.ts      # Vite 配置
├── tsconfig.json       # TS 配置
├── package.json
├── public/             # 静态资源（不会被打包）
└── src/
    ├── main.tsx        # JS 入口，把 <App /> 挂到 #root
    ├── App.tsx         # 根组件
    ├── App.css
    ├── index.css       # 全局样式
    └── assets/         # 会被打包的资源
```

`main.tsx` 长这样：

```tsx
// src/main.tsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
```

类比：`index.html` 是「**舞台**」，`<div id="root">` 是「**演出区**」，`createRoot().render(<App/>)` 是「**把演员（组件树）放上舞台**」。

`StrictMode` 是「**严苛模式**」——开发时会**故意**让组件渲染两次帮你发现副作用 bug，生产环境不会。

---

## 3. JSX：HTML 长在 JS 里

```tsx
const el = <h1 className="title">Hello, {name}</h1>
```

这就是 JSX——它**不是 HTML**，是 JS 语法糖。Vite（React 17+ 默认 automatic runtime）会编译成：

```js
// 现代产物（jsx-runtime，自动引入，不用 import React）
import { jsx as _jsx } from 'react/jsx-runtime'
const el = _jsx('h1', { className: 'title', children: ['Hello, ', name] })
```

> 旧资料里的 `React.createElement(...)` 是 classic runtime 产物——第 09 篇手写 mini-react 时
> 我们会**故意切回 classic**（`/** @jsx */` 指向自己的 createElement），那时再细说。

### 3.1 JSX 五条铁律

**① 花括号嵌入表达式**（不是语句）：

```tsx
const name = 'Tom'
<p>你好 {name}, 1+1={1 + 1}</p>          // ✅
<p>{ if (x) {...} }</p>                   // ❌ 不能写语句
<p>{ x > 0 ? '正' : '负' }</p>            // ✅ 三元是表达式
```

**② 单根元素**——一个组件 return 必须只有一个根：

```tsx
return <div><A/><B/></div>      // ✅
return <><A/><B/></>            // ✅ Fragment（不渲染额外标签）
return <A/><B/>                 // ❌ 编译报错
```

**③ class → className，for → htmlFor**（class 是 JS 关键字）。

**④ 自闭合标签必须斜杠**：`<img/>`、`<br/>`，不能 `<br>`。

**⑤ 属性驼峰**：`onclick → onClick`，`tabindex → tabIndex`。

---

## 4. 函数组件 vs 类组件

```tsx
// 类组件（旧，不学）
class Hello extends React.Component {
  render() { return <h1>Hi</h1> }
}

// 函数组件（现代，唯一推荐）
function Hello() {
  return <h1>Hi</h1>
}
```

理由：函数组件 + Hook 心智负担小，没有 `this` 烦恼，是 2026 年唯一标准。

---

## 5. Props：组件的参数

```tsx
// src/components/Greet.tsx
interface GreetProps {
  name: string
  age?: number          // ? = 可选
}

export function Greet({ name, age = 18 }: GreetProps) {
  return <p>{name} 今年 {age} 岁</p>
}
```

使用：

```tsx
import { Greet } from './components/Greet'

<Greet name="小明" />
<Greet name="小红" age={20} />
```

类比：组件是「**函数**」，props 是「**参数**」，UI 是「**返回值**」。

### 5.1 Children prop

```tsx
interface CardProps {
  title: string
  children: React.ReactNode
}

export function Card({ title, children }: CardProps) {
  return (
    <div className="card">
      <h3>{title}</h3>
      <div>{children}</div>
    </div>
  )
}

// 使用
<Card title="提示">
  <p>这里是任意内容</p>
  <button>关闭</button>
</Card>
```

`children` 是写在 `<Card>...</Card>` 中间的所有东西。

### 🔧 动手 1：写一个 `<Avatar src size name>` 组件

要求：size 默认 48，缺省 src 时显示 name 首字母。

<details>
<summary>答案</summary>

```tsx
// src/components/Avatar.tsx
interface Props { src?: string; size?: number; name: string }

export function Avatar({ src, size = 48, name }: Props) {
  const style = { width: size, height: size, borderRadius: '50%' }
  return src
    ? <img src={src} style={style} alt={name} />
    : <div style={{ ...style, background: '#888', color: '#fff',
        display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        {name[0].toUpperCase()}
      </div>
}
```
</details>

---

## 6. 条件渲染

```tsx
// 三元
{isLogin ? <Dashboard/> : <Login/>}

// && 短路
{hasError && <p style={{color:'red'}}>出错了</p>}

// 提前 return（推荐复杂场景）
function User({ user }: { user: User | null }) {
  if (!user) return <p>请登录</p>
  return <Profile user={user} />
}
```

⚠️ **&& 坑**：`{count && <Foo/>}` 当 count 是 0，会渲染出"0"！改成 `{count > 0 && <Foo/>}`。

---

## 7. 列表渲染 + key

```tsx
const todos = [
  { id: 1, text: '学 React' },
  { id: 2, text: '学 TS' },
]

return (
  <ul>
    {todos.map(t => <li key={t.id}>{t.text}</li>)}
  </ul>
)
```

**key 必须稳定唯一**——React 用 key 判断"哪个是哪个"，否则增删时会复用错组件，导致**输入框内容串行**。

⚠️ **千万别用 index 做 key**（除非列表完全静态）。

---

## 8. 组件拆分原则

「**一个组件只做一件事**」——SRP（单一职责）。

判断标准：「**这段 JSX 我能起一个清晰的名字吗？**」能就拆。

```tsx
// 坏：UserPage 啥都管
function UserPage() { return <div>{/* 100 行 */}</div> }

// 好：拆开
function UserPage() {
  return <><UserHeader/><UserPosts/><UserFooter/></>
}
```

---

## 9. 受控 vs 非受控组件

```tsx
// 受控（推荐）：值由 React state 控制
const [v, setV] = useState('')
<input value={v} onChange={e => setV(e.target.value)} />

// 非受控：值由 DOM 自己管，用 ref 取
const ref = useRef<HTMLInputElement>(null)
<input ref={ref} defaultValue="hi" />
<button onClick={() => alert(ref.current?.value)}>读</button>
```

类比：受控 = 「**遥控车**」，每一帧都听你的；非受控 = 「**惯性玩具车**」，自己跑。

99% 用受控；表单大、性能敏感时用非受控（第 05 篇 React Hook Form 就是非受控）。

---

## 10. React DevTools

Chrome 扩展商店搜 "React Developer Tools" 装上。多两个面板：
- **Components**：看组件树、实时改 props/state
- **Profiler**：录一段操作，看哪个组件渲染了几次、多慢

调试 React 必备，**今天就装**。

---

## 11. 实战：Todo 最简版

```tsx
// src/App.tsx
import { useState } from 'react'

interface Todo { id: number; text: string; done: boolean }

export default function App() {
  const [todos, setTodos] = useState<Todo[]>([])
  const [input, setInput] = useState('')

  const add = () => {
    if (!input.trim()) return
    setTodos([...todos, { id: Date.now(), text: input, done: false }])
    setInput('')
  }

  const toggle = (id: number) =>
    setTodos(todos.map(t => t.id === id ? { ...t, done: !t.done } : t))

  const remove = (id: number) =>
    setTodos(todos.filter(t => t.id !== id))

  return (
    <div style={{ maxWidth: 400, margin: '40px auto' }}>
      <h1>Todo</h1>
      <input value={input} onChange={e => setInput(e.target.value)}
             onKeyDown={e => e.key === 'Enter' && add()} />
      <button onClick={add}>添加</button>
      <ul>
        {todos.map(t => (
          <li key={t.id}>
            <input type="checkbox" checked={t.done} onChange={() => toggle(t.id)} />
            <span style={{ textDecoration: t.done ? 'line-through' : 'none' }}>
              {t.text}
            </span>
            <button onClick={() => remove(t.id)}>删</button>
          </li>
        ))}
      </ul>
    </div>
  )
}
```

把它粘进 StackBlitz 的 vite-react-ts 模板，立刻能跑。

### 🔧 动手 2：扩展 Todo

加一个"全部完成 / 未完成 / 全部"过滤按钮。

<details>
<summary>提示</summary>

```tsx
新增 `const [filter, setFilter] = useState<'all'|'done'|'todo'>('all')`，渲染前 `todos.filter(...)`。
```
</details>

### 🔧 动手 3：拖拽排序（原生 HTML5 DnD，T1 闭环）

不用任何库——`draggable` + 三个事件 + 一个记住来源下标的 ref：

<details><summary>参考实现</summary>

```tsx
import { useRef, useState } from 'react'

function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([])
  const dragIdx = useRef<number | null>(null)

  const onDrop = (to: number) => {
    const from = dragIdx.current
    dragIdx.current = null
    if (from === null || from === to) return
    setTodos(list => {
      const next = [...list]
      const [moved] = next.splice(from, 1)
      next.splice(to, 0, moved)
      return next
    })
  }

  return (
    <ul>
      {todos.map((t, i) => (
        <li key={t.id} draggable
            onDragStart={() => (dragIdx.current = i)}
            onDragOver={e => e.preventDefault()}
            onDrop={() => onDrop(i)}>
          {t.text}
        </li>
      ))}
    </ul>
  )
}
```
</details>

T1 三要素至此全有教学承担：过滤（动手 2）+ 拖拽排序（本节）+ 本地持久化（第 03 篇 §1 `useLocalStorage`，把 useState 换掉即可）。

### 🔧 动手 4：计算器（本周第二产出）

需求：显示屏 + 0-9 + 四则运算 + `C` 清零 + `=` 求值，支持连续计算（`2 + 3 ×` 要先算出 5）。
状态就三个：`display`（屏上内容）、`prev`（第一个操作数）、`op`（待算符），外加一个「刚按完运算符，下一个数字要另起」的 `fresh` 标志——这是计算器状态机的灵魂。

<details><summary>参考实现（先自己写再对答案）</summary>

```tsx
import { useState } from 'react'

const KEYS = ['7', '8', '9', '÷', '4', '5', '6', '×', '1', '2', '3', '-', '0', '.', '=', '+', 'C']

const compute = (a: number, b: number, op: string) =>
  op === '+' ? a + b : op === '-' ? a - b : op === '×' ? a * b : a / b

export default function Calculator() {
  const [display, setDisplay] = useState('0')
  const [prev, setPrev] = useState<number | null>(null)
  const [op, setOp] = useState<string | null>(null)
  const [fresh, setFresh] = useState(true)

  const press = (k: string) => {
    if (/[\d.]/.test(k)) {
      setDisplay(s => (fresh || s === '0' || s === 'Error' ? k : s + k))
      setFresh(false)
    } else if (k === 'C') {
      setDisplay('0'); setPrev(null); setOp(null); setFresh(true)
    } else if (k === '=') {
      if (prev === null || !op) return
      const r = compute(prev, Number(display), op)
      setDisplay(Number.isFinite(r) ? String(Math.round(r * 1e10) / 1e10) : 'Error')
      setPrev(null); setOp(null); setFresh(true)
    } else {                                   // 运算符
      if (prev !== null && op && !fresh) {     // 连续计算：先把上一步算掉
        const r = compute(prev, Number(display), op)
        setPrev(r); setDisplay(String(r))
      } else {
        setPrev(Number(display))
      }
      setOp(k); setFresh(true)
    }
  }

  return (
    <div style={{ width: 220, margin: '40px auto' }}>
      <input value={display} readOnly style={{ width: '100%', fontSize: 24, textAlign: 'right' }} />
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 4, marginTop: 8 }}>
        {KEYS.map(k => <button key={k} onClick={() => press(k)}>{k}</button>)}
      </div>
    </div>
  )
}
```
</details>

小练习：上面的 `press` 允许按出两个小数点（`1.2.3`）——加一行拦截它。

## 周末检查

### ✅ Checklist
- [ ] 能讲清"声明式 vs 命令式"
- [ ] 用 Vite 起了一个 React-TS 项目
- [ ] 知道 JSX 五条规则
- [ ] 写过 ≥5 个函数组件，会用 Props 和 children
- [ ] 列表渲染懂 key
- [ ] 装好了 React DevTools
- [ ] Todo 实战跑通
- [ ] Todo 能拖拽排序（动手 3）
- [ ] 计算器跑通，连续计算不丢数（动手 4）

### 🐛 错误清单
- "Each child should have unique key" → map 没加 key
- "Objects are not valid as a React child" → 直接 `{obj}` 渲对象，要 `{obj.name}`
- 输入框无法输入 → 写了 value 没写 onChange，或 value={undefined}
- `cannot read properties of null` → `useRef` 初始用得太早，加 `?.` 或 `if(ref.current)`

### 📚 资源
- 官方教程（**必读**）：<https://react.dev/learn>
- 中文版：<https://zh-hans.react.dev/>
- 《React 设计原理》卡颂 - 进阶
- StackBlitz：<https://stackblitz.com/> 在线练手
