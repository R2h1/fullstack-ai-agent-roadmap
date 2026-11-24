---
title: 手写 mini-react v1（Fiber 核心）
type: weekly-tutorial
chapter: "04"
chapter_title: React 从使用到源码
order: 10
week: 9
duration: 7 天
difficulty: ⭐⭐⭐⭐⭐
prerequisites:
  - 第 08 篇
outputs:
  - mini-react
tags: [react, fiber, mini-react, jsx, reconciler, scheduler, requestIdleCallback]
prev: "[[08-性能优化]]"
next: "[[10-手写mini-react-v2]]"
created: 2026-06-19
updated: 2026-06-19
---

# 第 09 篇 · 手写 mini-react v1（Fiber 核心）

> "**用过 ≠ 懂**"。本周用 ~300 行代码复刻一个能跑的小 React，
> 直到你能在白板上画出 Fiber 树。

---

## 一、为什么要手写

- 面试常问"React 怎么不卡"——背答案没用，写过才能答得自然。
- 看官方源码（几十万行）会劝退；先写**乞丐版**，再去看源码就像看注释。
- 真正吃透三件事：**JSX、Fiber、调度**。

---

## 二、React 整体架构（必背）

```
JSX
 │  Babel/SWC 编译
 ▼
React.createElement(...)        ← Element Tree（虚拟 DOM 描述）
 │  Reconciler（协调器）         ← 把 Element 转成 Fiber 链表，标记差异
 ▼
Fiber Tree
 │  Scheduler（调度器）          ← 决定何时干活，能中断
 ▼
Renderer（渲染器：react-dom / react-native）
 │  commit
 ▼
真实 DOM
```

类比一次装修：
- **JSX** = 户型图（你画的）
- **Element** = 设计稿（机器看的）
- **Reconciler** = 设计师（拆步骤）
- **Scheduler** = 项目经理（排期，可暂停）
- **Renderer** = 工人（真砸墙）

---

## 三、第 1 步：JSX 转换 + 自己实现 createElement

JSX 不是 React 语法，是 Babel/SWC 把它编译成函数调用：

```tsx
const el = <div id="x">hi <b>!</b></div>
// 等价于
const el = React.createElement('div', { id: 'x' }, 'hi ', React.createElement('b', null, '!'))
```

**自己实现**：

```ts
// src/mini-react.ts

// Props 约定：所有属性 + children 数组。
// children 是「函数式组件里 props.children」的来源 —— 后面 render 时子元素全从这里拿。
type Props = Record<string, any> & { children: any[] }

// Element 就是「虚拟 DOM 节点」：一个普通 JS 对象。
// 注意 type 可以是 string（原生标签，如 'div'）或 Function（函数组件）。
type Element = { type: string | Function, props: Props }

// JSX 编译后长这样：
//   <div id="a">hello</div>
//   → createElement('div', { id: 'a' }, 'hello')
// 所以 JSX 的「第一个参数是标签」，和这里签名完全对应。
function createElement(type: any, props: any, ...children: any[]): Element {
  return {
    type,
    props: {
      ...props,
      // 覆盖 props.children —— 即使调用方手写了 children 属性，也以「JSX 子元素」为准
      // （React 本身也是这样：props.children 是编译器给的，不是手写的）。
      children: children
        // ① 扁平化一层：处理 <ul>{items.map(...)}</ul> 这种「数组作为子元素」。
        //    但 flat() 默认只拍平一层 —— 嵌套两层的数组不会被完全拍平（见第 2 条）。
        .flat()
        // ② 非对象 → 包成文本节点；对象（Element）原样保留。
        //    ⚠️ 这里有三个隐患，见下文第 1 条：
        //    - null / undefined：typeof 为 'object'，被当成 Element 保留，后面 render 崩
        //    - boolean：typeof 为 'boolean'，被包成 TEXT_ELEMENT，渲染出 "true"/"false"
        //    - 数组里嵌套数组：flat() 只拍平一层
        .map(c =>
          typeof c === 'object' ? c : createTextElement(c)
        ),
    },
  }
}

// 文本节点也是 Element，只是 type 固定为 'TEXT_ELEMENT'。
// 后面 render 时靠这个 type 区分「创建文本节点」还是「创建元素节点」。
// 用 nodeValue 而不是 children —— 文本节点没有子元素，直接存值更直接。
function createTextElement(text: string | number | boolean) {
  return {
    type: 'TEXT_ELEMENT',
    props: { nodeValue: text, children: [] },
  }
}

// 默认导出成对象，是为了让 JSX 的「自动导入」能找到 createElement。
// Babel / TypeScript 的 jsxFactory 配置会生成 `MiniReact.createElement(...)`。
export default { createElement }
```

让 Vite/TS 用我们的版本：

```jsonc
// tsconfig.json
{ "compilerOptions": {
  "jsx": "react",
  "jsxFactory": "MiniReact.createElement"
}}
```

```tsx
// main.tsx
/** @jsx MiniReact.createElement */
import MiniReact from './mini-react'
const el = <div id="x">hi <b>!</b></div>
console.log(el)
```

控制台会看到一棵嵌套对象，这就是 Element Tree。

---

## 四、第 2 步：Element → DOM（递归版，演示问题）

```ts
function render(el: Element, container: HTMLElement) {
  const dom: any = el.type === 'TEXT_ELEMENT'
    ? document.createTextNode('')
    : document.createElement(el.type as string)

  const isProperty = (k: string) => k !== 'children'
  Object.keys(el.props).filter(isProperty).forEach(name => {
    if (name.startsWith('on')) {
      dom.addEventListener(name.toLowerCase().slice(2), el.props[name])
    } else {
      dom[name] = el.props[name]
    }
  })

  el.props.children.forEach(c => render(c, dom))
  container.appendChild(dom)
}
```

跑通了，但有大问题：**递归一旦开始就停不下来**。组件树一深，主线程被堵几百毫秒，按钮都点不动。
这就是 **Fiber 出现的原因**。

---

## 五、第 3 步：Fiber 是什么

把递归的"调用栈"，**改成可遍历的链表**。每个 Fiber 节点长这样：

```ts
type Fiber = {
  // ─── 描述「这个节点是什么」───
  type: string | Function
  // 和 Element 的 type 一致：'div' / 'TEXT_ELEMENT' / 函数组件。
  // 它是「创建 DOM 时用什么」的依据。

  props: Props
  // 和 Element 的 props 一致：属性 + children。
  // 注意 children 在这里是「待调和的子 Element 数组」，不是 Fiber 数组 ——
  // 子 Fiber 是通过下面的 child / sibling 指针连起来的。

  // ─── 指向「已经存在的真实 DOM」───
  dom: HTMLElement | Text | null
  // 函数组件的 Fiber 没有自己的 DOM —— 它返回的 Element 才有。
  // 所以函数组件 Fiber 的 dom 是 null，它的子 Fiber 才有真实 DOM。

  // ─── 树结构，但用「链表」表达 ───
  parent: Fiber | null
  // 父 Fiber。用于「向上冒泡」—— 比如 commit 阶段从根一路找下去，
  // 或者「找下一个要处理的节点」时回溯。

  child: Fiber | null
  // 第一个子 Fiber。
  // ⚠️ 注意：只有「第一个」—— 后续兄弟通过 sibling 链走。

  sibling: Fiber | null
  // 下一个兄弟 Fiber。
  // child + sibling 合起来等价于「children 数组」，但可以「逐个处理、随时中断」。

  // ─── 双缓冲：指向「上一次渲染的自己」───
  alternate: Fiber | null
  // 上一次 commit 后的 Fiber。新 Fiber 和 alternate 配对做 diff：
  //   - 同一个位置，old fiber 和 new fiber 的 type 相同 → 复用 DOM，打 UPDATE
  //   - type 不同 → 删旧的，建新的，打 PLACEMENT
  // 根 Fiber 的 alternate 是「上一次的根」，这是「哪棵树是当前树」的锚点。

  // ─── 本次渲染要对这个节点做什么 ───
  effectTag?: 'PLACEMENT' | 'UPDATE' | 'DELETION'
  // PLACEMENT：新建 DOM，commit 时 appendChild
  // UPDATE：复用 DOM，只更新变化的属性/事件
  // DELETION：删除 DOM，commit 时 removeChild
  // ⚠️ 没有 effectTag 表示「这个节点没变化」—— commit 时跳过
}
```

三个指针（**画图记**）：

```
     A
    /
   B───C───D       (B.sibling = C, C.sibling = D)
  /
 E
```
- `child`：第一个孩子
- `sibling`：右边的兄弟
- `return` / `parent`：父节点

遍历顺序（深度优先）：A → B → E → C → D。每访问一个节点 = **一个工作单元 (unit of work)**。

---

## 六、第 4 步：双缓冲（current vs workInProgress）

> 一边渲染，一边页面照常跑，怎么不打架？**两棵树**。

- `current` 树 = 屏幕上当前在用的。
- `wipRoot` 树 = 正在构建的下一版。
- 构建完整棵 wip 后，**一次性切换**（commit），用户看到无闪烁更新。

```
current ──┐         wipRoot ──┐
   App    │             App   │
   /\     │             /\    │
  H  M    │            H  M'  │  ← M 改了，标 UPDATE
```

每个 wip Fiber 的 `alternate` 指回 current 同位置的 Fiber，diff 时方便比较。

---

## 七、第 5 步：requestIdleCallback 调度

浏览器每帧大概 16.6ms。React 的承诺：**渲染可以中断，让浏览器先处理用户输入**。

```ts
// ── 调度状态 ──
let nextUnitOfWork: Fiber | null = null
// 「下一个要处理的工作单元」。performUnitOfWork 处理完当前节点后返回它，
// workLoop 拿它继续下一轮。为 null 表示「这棵树处理完了」。

let wipRoot: Fiber | null = null
// Work In Progress Root —— 「正在构建的新树」的根。
// 和屏幕上当前的树（currentRoot）并存，构建完才一次性切换（双缓冲）。
// 它同时是「是否还有未提交的树」的标志：非 null 说明有活要干/要提交。


function workLoop(deadline: IdleDeadline) {
  let shouldYield = false

  // 核心循环：只要还有工作、且这一帧还有时间，就继续处理
  while (nextUnitOfWork && !shouldYield) {
    // performUnitOfWork 做三件事：
    //   ① 给当前 fiber 创建 DOM / 更新属性
    //   ② 为 children 创建子 fiber（diff）
    //   ③ 返回「下一个要处理的 fiber」
    // 返回值的设计是精髓：把递归变成了「迭代 + 外部状态机」
    nextUnitOfWork = performUnitOfWork(nextUnitOfWork)

    // 剩余空闲时间不足 1ms → 让出主线程，避免掉帧
    // 循环退出后，nextUnitOfWork 仍非 null，下一帧的 workLoop 会接着跑
    shouldYield = deadline.timeRemaining() < 1
  }

  // 所有工作单元处理完（nextUnitOfWork 为 null），且有待提交的树 → 提交
  // 两个条件缺一不可：只有 nextUnitOfWork 为 null 才是「这棵树构建完了」
  if (!nextUnitOfWork && wipRoot) commitRoot()

  // ⚠️ 必须重新注册，否则只会在第一帧跑一次
  requestIdleCallback(workLoop)
}

requestIdleCallback(workLoop)
```

> 真实 React 不用 `requestIdleCallback`（兼容性差、调度时机不准），自己写了 Scheduler 包基于 `MessageChannel`。这里我们用 `requestIdleCallback` 演示概念。

---

## 八、performUnitOfWork：一次干一点活

```ts
function performUnitOfWork(fiber: Fiber): Fiber | null {
  // 1. 给当前 fiber 创建 DOM（先不挂载到页面）
  if (!fiber.dom) fiber.dom = createDom(fiber)

  // 2. 给 children 创建 fiber，串成链表
  reconcileChildren(fiber, fiber.props.children)

  // 3. 返回下一个工作单元：child > sibling > parent.sibling
  if (fiber.child) return fiber.child
  let next: Fiber | null = fiber
  while (next) {
    if (next.sibling) return next.sibling
    next = next.parent
  }
  return null
}

function createDom(fiber: Fiber) {
  const dom: any = fiber.type === 'TEXT_ELEMENT'
    ? document.createTextNode('')
    : document.createElement(fiber.type as string)
  updateDom(dom, { children: [] }, fiber.props)
  return dom
}

function reconcileChildren(wipFiber: Fiber, children: Element[]) {
  let prevSibling: Fiber | null = null
  children.forEach((child, i) => {
    const newFiber: Fiber = {
      type: child.type,
      props: child.props,
      dom: null,
      parent: wipFiber,
      child: null,
      sibling: null,
      alternate: null,
      effectTag: 'PLACEMENT',
    }
    if (i === 0) wipFiber.child = newFiber
    else prevSibling!.sibling = newFiber
    prevSibling = newFiber
  })
}
```

**关键点**：**不要在 performUnitOfWork 里挂载 DOM**——挂一半被中断，用户会看到残缺页面。

---

## 九、第 6 步：commit 阶段

构建完整棵 wip 后，**一次同步**地把 DOM 全挂上去：

```ts
function commitRoot() {
  commitWork(wipRoot!.child)
  wipRoot = null
}

function commitWork(fiber: Fiber | null) {
  if (!fiber) return
  let parentFiber = fiber.parent
  while (parentFiber && !parentFiber.dom) parentFiber = parentFiber.parent  // 跳过函数组件
  const parentDom = parentFiber!.dom!

  if (fiber.effectTag === 'PLACEMENT' && fiber.dom) {
    parentDom.appendChild(fiber.dom)
  }
  // UPDATE / DELETION 等 v2 再加

  commitWork(fiber.child)
  commitWork(fiber.sibling)
}
```

---

## 十、对外 API：render

```ts
function render(el: Element, container: HTMLElement) {
  wipRoot = {
    type: 'HOST_ROOT' as any,
    props: { children: [el] },
    dom: container,
    parent: null, child: null, sibling: null, alternate: null,
  }
  nextUnitOfWork = wipRoot
}

export default { createElement, render }
```

跑 demo（计数器先用回调写死，下周再实现 hooks）：

```tsx
/** @jsx MiniReact.createElement */
import MiniReact from './mini-react'

const container = document.getElementById('app')!
let n = 0
function rerender() {
  const el = (
    <div>
      <h1>计数: {n}</h1>
      <button onClick={() => { n++; rerender() }}>+1</button>
    </div>
  )
  MiniReact.render(el, container)
}
rerender()
```

打开浏览器，点按钮——成了。**你写出了一个能跑的 React。**

---

## 十一、画图理解（务必动手画）

练习：在纸上画下面这棵树的 Fiber 结构（含 child/sibling/return 三个指针），并写出 `performUnitOfWork` 的访问顺序：

```tsx
<App>
  <Header>
    <Logo/>
    <Nav/>
  </Header>
  <Main>
    <Article/>
  </Main>
</App>
```

---

## 周末 Checklist

- [ ] 自己实现的 `createElement` 输出对的 Element Tree
- [ ] 跑通递归版 `render`
- [ ] 能口头解释为什么递归 render 会卡
- [ ] 能在白板上画 Fiber 三指针
- [ ] 能写出 `performUnitOfWork` 的"child / sibling / parent" 三档返回
- [ ] 能解释双缓冲（current vs wip）
- [ ] commit 阶段一次性挂载 DOM 跑通
- [ ] 计数器 demo 能跑

## 常见错误

| 现象 | 原因 | 解法 |
| --- | --- | --- |
| JSX 不识别 `MiniReact` | tsconfig `jsx`/`jsxFactory` 没改，或文件没加 `/** @jsx */` 注释 | 二选一加上 |
| 页面渲染一半 | 在 `performUnitOfWork` 里 appendChild | 移到 `commitRoot` |
| children 是字符串报错 | 没把字符串转 TEXT_ELEMENT | `createTextElement` 别忘 |
| 死循环 | sibling/parent 链断了 | 检查 `prevSibling.sibling = newFiber` |

## 资源
- Build your own React (didact)：https://pomb.us/build-your-own-react/
- big-react（卡颂手把手版）：https://github.com/BetaSu/big-react
- React 源码导读：https://react.iamkasong.com/
- React 团队 RFC：https://github.com/reactjs/rfcs
