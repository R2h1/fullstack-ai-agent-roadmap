---
title: CSS 进阶与动画
type: weekly-tutorial
chapter: "03"
chapter_title: HTML / CSS 现代 Web
order: 4
week: 3
duration: 7 天
daily_hours: 2
difficulty: ⭐⭐⭐
prerequisites:
  - 第 02 篇
goals:
  - 让网页"会动"。掌握主题切换、过渡、关键帧动画、滚动驱动动画，并交付纯 CSS 组件四件套（T3）。
outputs:
  - 纯 CSS 组件四件套（模态框/手风琴/开关/步骤条，T3）
tags: [CSS变量, 暗黑模式, 动画, transform, transition, 容器查询]
prev: "[[02-CSS基础与Flex-Grid]]"
next: "[[04-Tailwind与渲染原理]]"
created: 2026-06-19
updated: 2026-11-28
---

# 第 03 篇 · CSS 进阶与动画

> 学习目标：让网页"会动"。掌握主题切换、过渡、关键帧动画、滚动驱动动画。

---

## 一、CSS 变量 var(--name)

### 1.1 基础语法

```css
:root {
  --primary: #2563eb;
  --radius: 8px;
  --gap: 16px;
}

.button {
  background: var(--primary);
  border-radius: var(--radius);
  padding: var(--gap);
}
```

`:root` ≈ `<html>`，**全局变量**写在这里。

### 1.2 局部变量

```css
.card {
  --card-padding: 24px;
  padding: var(--card-padding);
}
.card.compact {
  --card-padding: 12px;   /* 覆盖 */
}
```

### 1.3 与 JS 交互

```js
document.documentElement.style.setProperty('--primary', '#ff0000');
```

变量可被 JS 动态改变，**整个网站颜色立即换肤**。

---

## 二、主题切换（暗黑模式）

### 2.1 系统偏好探测

```css
@media (prefers-color-scheme: dark) {
  body { background: #0a0a0a; color: #f5f5f5; }
}
```

### 2.2 现代写法 light-dark()

```css
:root {
  color-scheme: light dark;
}
body {
  background: light-dark(#fff, #0a0a0a);
  color: light-dark(#0a0a0a, #fff);
}
```

一行解决浅色/深色，不用写媒体查询！

### 2.3 完整切换实战

```html
<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
<meta charset="UTF-8">
<style>
  :root {
    --bg: #ffffff;
    --text: #0a0a0a;
    --card: #f5f5f5;
  }
  [data-theme="dark"] {
    --bg: #0a0a0a;
    --text: #f5f5f5;
    --card: #1a1a1a;
  }
  body {
    background: var(--bg);
    color: var(--text);
    transition: background .3s, color .3s;  /* 平滑过渡 */
    font-family: sans-serif;
    padding: 32px;
  }
  .card {
    background: var(--card);
    padding: 24px;
    border-radius: 8px;
    margin-top: 16px;
  }
  button {
    padding: 8px 16px;
    border: 0;
    border-radius: 6px;
    cursor: pointer;
  }
</style>
</head>
<body>
  <button onclick="toggleTheme()">切换主题</button>
  <div class="card">这是一张卡片</div>

  <script>
    function toggleTheme() {
      const html = document.documentElement;
      const next = html.dataset.theme === 'light' ? 'dark' : 'light';
      html.dataset.theme = next;
      localStorage.setItem('theme', next);
    }
    // 启动时：用户存过 → 用存的；没存过 → 跟随系统偏好（T4 的"系统偏好检测"）
    document.documentElement.dataset.theme =
      localStorage.getItem('theme')
      || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    // 可选进阶：没手动选过的人，系统切深色时页面跟着切
    matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
      if (!localStorage.getItem('theme'))
        document.documentElement.dataset.theme = e.matches ? 'dark' : 'light';
    });
  </script>
</body>
</html>
```

---

## 三、选择器进阶

### 3.1 :has() —— 父选择器（终于来了）

```css
/* 卡片里有图片时去掉 padding */
.card:has(img) { padding: 0; }

/* 表单中的 input 聚焦时高亮 label */
label:has(input:focus) { color: blue; }

/* 列表项被勾选 */
li:has(input:checked) { background: yellow; }
```

### 3.2 :is() / :where()

```css
/* 旧 */
header h1, header h2, header h3 { color: red; }

/* 新 */
header :is(h1, h2, h3) { color: red; }

/* :where() 与 :is() 一样，但优先级为 0 —— 容易被覆盖 */
:where(article) p { line-height: 1.6; }
```

### 3.3 :not()

```css
li:not(.active) { color: gray; }
button:not([disabled]):hover { background: blue; }
```

---

## 四、容器查询 @container（新一代响应式）

### 4.1 痛点

媒体查询基于**视口**，但卡片本身可能在侧栏 / 主区，宽度不同样式应不同。

### 4.2 写法

```css
.parent {
  container-type: inline-size;   /* 声明为容器 */
  container-name: card;
}

@container card (min-width: 400px) {
  .card { display: flex; gap: 16px; }
}
```

**卡片的样式根据它所在的容器宽度变**，而不是整个屏幕。组件复用之神。

---

## 五、逻辑属性

中文从左到右、阿拉伯文从右到左。**逻辑属性自动适配**。

| 物理 | 逻辑 |
|------|------|
| `margin-left` | `margin-inline-start` |
| `margin-right` | `margin-inline-end` |
| `margin-top` | `margin-block-start` |
| `padding-left/right` | `padding-inline` |
| `padding-top/bottom` | `padding-block` |

```css
/* 不要再写 */
.box { margin-left: 16px; margin-right: 16px; }

/* 写这个 */
.box { margin-inline: 16px; }
```

---

## 六、transform 变换

### 6.1 四大基础

```css
transform: translate(100px, 50px);  /* 平移 */
transform: rotate(45deg);            /* 旋转 */
transform: scale(1.5);               /* 缩放 */
transform: skew(20deg);              /* 倾斜 */

/* 组合 */
transform: translate(50%, -50%) rotate(45deg) scale(1.2);
```

```
原始：    rotate(15deg):    scale(1.3):     translate(20,0):
┌──┐         ┌──┐             ┌──────┐          ┌──┐
│A │          \A \             │  A   │   ····   │A │
└──┘           └──┘             └──────┘          └──┘
```

### 6.2 3D 变换

```css
.card {
  transform: perspective(800px) rotateY(20deg);
}

.parent {
  perspective: 1000px;   /* 设在父元素上效果更稳 */
}
```

`perspective` 越小越夸张（像把眼睛凑近）。

### 6.3 transform-origin

变换的"轴心"，默认是元素中心。

```css
.box {
  transform-origin: top left;   /* 从左上角旋转 */
  transform: rotate(45deg);
}
```

---

## 七、transition 过渡

> 当一个属性"改变"时，让它"花点时间"过渡，而不是瞬间变。

```css
.btn {
  background: blue;
  transition: background 0.3s ease, transform 0.2s;
}
.btn:hover {
  background: red;
  transform: scale(1.1);
}
```

### 7.1 四个属性

```css
transition-property: background;     /* 哪个属性 */
transition-duration: 0.3s;            /* 多久 */
transition-timing-function: ease;     /* 缓动 */
transition-delay: 0.1s;               /* 延迟 */

/* 缩写 */
transition: background 0.3s ease 0.1s;
```

### 7.2 缓动函数

| 关键字 | 曲线 | 感觉 |
|--------|------|------|
| `linear` | 匀速 | 机械 |
| `ease` | 慢-快-慢 | 默认，自然 |
| `ease-in` | 慢-快 | 启动慢 |
| `ease-out` | 快-慢 | 减速到位 |
| `cubic-bezier(.68,-.55,.27,1.55)` | 自定义 | 反弹效果 |

可视化网站：https://cubic-bezier.com

### 7.3 动手任务 1：弹跳按钮

```css
.btn {
  padding: 12px 24px;
  background: #2563eb;
  color: white;
  border: 0;
  border-radius: 8px;
  transition: transform 0.3s cubic-bezier(.68,-.55,.27,1.55);
  cursor: pointer;
}
.btn:hover { transform: scale(1.1) rotate(-2deg); }
.btn:active { transform: scale(0.95); }
```

---

## 八、@keyframes 关键帧动画

> transition 只能管"两点之间"。复杂动画用 @keyframes。

### 8.1 基础

```css
@keyframes bounce {
  0%   { transform: translateY(0); }
  50%  { transform: translateY(-30px); }
  100% { transform: translateY(0); }
}

.ball {
  animation: bounce 1s ease infinite;
}
```

### 8.2 全部属性

```css
animation-name: bounce;
animation-duration: 1s;
animation-timing-function: ease;
animation-delay: 0s;
animation-iteration-count: infinite;   /* 或数字 */
animation-direction: alternate;        /* 来回 */
animation-fill-mode: forwards;         /* 停在最后一帧 */
animation-play-state: running;         /* 或 paused */

/* 缩写 */
animation: bounce 1s ease 0s infinite alternate forwards;
```

### 8.3 案例：加载旋转图标

```css
@keyframes spin {
  to { transform: rotate(360deg); }
}
.spinner {
  width: 32px;
  height: 32px;
  border: 4px solid #e5e7eb;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
```

---

## 九、滤镜 filter

### 9.1 基础滤镜

```css
filter: blur(5px);              /* 模糊 */
filter: brightness(1.2);         /* 亮度 */
filter: contrast(1.5);           /* 对比 */
filter: grayscale(100%);         /* 灰度 */
filter: hue-rotate(90deg);       /* 色相 */
filter: drop-shadow(0 4px 8px #0008);

/* 组合 */
filter: blur(2px) brightness(0.8);
```

### 9.2 backdrop-filter（毛玻璃）

```css
.glass {
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(20px);    /* 给元素**后面**的内容模糊 */
  border: 1px solid rgba(255,255,255,0.4);
  border-radius: 16px;
}
```

iOS 风格毛玻璃效果一行搞定。

---

## 十、渐变

```css
/* 线性 */
background: linear-gradient(135deg, #ff6b6b, #4ecdc4);

/* 径向 */
background: radial-gradient(circle at center, yellow, red);

/* 锥形 */
background: conic-gradient(red, yellow, green, blue, red);

/* 多色 + 位置 */
background: linear-gradient(to right, red 0%, yellow 50%, green 100%);
```

可视化生成：https://cssgradient.io

---

## 十一、阴影

### 11.1 box-shadow

```css
/* x偏移  y偏移  模糊  扩散  颜色 */
box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);

/* 多层叠加更立体 */
box-shadow:
  0 1px 2px rgba(0,0,0,.05),
  0 4px 8px rgba(0,0,0,.08),
  0 16px 32px rgba(0,0,0,.12);

/* 内阴影 */
box-shadow: inset 0 2px 4px rgba(0,0,0,.2);
```

### 11.2 text-shadow

```css
text-shadow:
  0 1px 0 #ccc,
  0 2px 0 #c9c9c9,
  0 5px 10px rgba(0,0,0,.3);
```

---

## 十二、其他黑科技

### 12.1 clip-path 剪切

```css
.triangle { clip-path: polygon(50% 0, 100% 100%, 0 100%); }
.circle   { clip-path: circle(50%); }
.diamond  { clip-path: polygon(50% 0, 100% 50%, 50% 100%, 0 50%); }
```

可视化：https://bennettfeely.com/clippy

### 12.2 mix-blend-mode

```css
.text-overlay {
  mix-blend-mode: difference;  /* 像 PS 的"差值"图层 */
  color: white;
}
```

### 12.3 scroll-snap

```css
.container {
  scroll-snap-type: x mandatory;
  overflow-x: auto;
  display: flex;
}
.slide {
  scroll-snap-align: center;
  flex: 0 0 100%;
}
```

像滑屏 App 一样按页吸附。

---

## 十三、本周大实战

### 13.1 纯 CSS 模态框（无 JS）

利用 `:target` 伪类：

```html
<a href="#modal">打开</a>
<div id="modal" class="modal">
  <div class="modal-content">
    <a href="#" class="close">×</a>
    <h2>这是模态框</h2>
  </div>
</div>

<style>
.modal {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  pointer-events: none;
  transition: opacity .3s;
}
.modal:target {
  opacity: 1;
  pointer-events: auto;
}
.modal-content {
  background: white;
  padding: 32px;
  border-radius: 12px;
  position: relative;
  transform: scale(.8);
  transition: transform .3s;
}
.modal:target .modal-content { transform: scale(1); }
.close {
  position: absolute;
  top: 8px; right: 16px;
  font-size: 24px;
  text-decoration: none;
  color: #666;
}
</style>
```

### 13.2 Apple 风格按钮

```html
<button class="apple-btn">购买 →</button>

<style>
.apple-btn {
  padding: 14px 32px;
  background: linear-gradient(180deg, #007aff, #0051d5);
  color: white;
  border: 0;
  border-radius: 980px;       /* 大圆角变胶囊 */
  font-size: 17px;
  font-weight: 500;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(0, 122, 255, 0.4);
  transition: all .25s;
}
.apple-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 122, 255, 0.5);
}
.apple-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(0, 122, 255, 0.4);
}
</style>
```

### 13.3 滚动驱动动画（scroll-driven animations）

> ⚠️ 旧提案的 `@scroll-timeline` at-rule **已废弃**——现行标准是下面这个 `animation-timeline` 属性写法。

```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(40px); }
  to   { opacity: 1; transform: translateY(0); }
}
.section {
  animation: fadeIn linear;
  animation-timeline: view();      /* 元素进入视口时触发 */
  animation-range: entry 0% cover 30%;
}
```

**支持度要心里有数**（caniuse 口径，2026-11）：Chrome / Edge（115+）完整支持；Firefox 新版本已跟进；**Safari 仍未落地**。做章项目（Apple/Stripe 页）时，面向 Safari 用户要么接受"静态也能看"（动画只是锦上添花，内容不依赖它），要么用 JS 兜底——最省事的兜底就是 IntersectionObserver 加个类：

```javascript
// 兜底：不支持 animation-timeline 时，进视口加 .in 类触发普通 transition
const supported = CSS.supports('animation-timeline', 'view()');
if (!supported) {
  const io = new IntersectionObserver(es => es.forEach(e =>
    e.isIntersecting && e.target.classList.add('in')), { threshold: 0.2 });
  document.querySelectorAll('.section').forEach(el => io.observe(el));
}
```
```css
.section.in { opacity: 1; transform: none; transition: .6s ease; }
```

> 🎯 章项目 B/C 的**视差、滚动驱动缩放、GSAP/Lenis 完整工作流**见第 04 篇 §十六「章项目集成」——那里是主战场，本节先把 CSS 原生方案装进工具箱。

### 13.4 两个漏补的现代特性：CSS 嵌套 与 subgrid

**CSS 原生嵌套**（2023 起全浏览器可用，别再只会 Sass）：

```css
.card {
  padding: 24px;
  & h3 { margin: 0 0 8px; }              /* & = 父选择器 */
  &:hover { box-shadow: 0 8px 24px #0002; }
  .price { color: oklch(60% .2 145); }   /* 后代直接写 */
}
```

**subgrid：让嵌套网格对齐父网格的列**。章项目里「卡片网格的标题/价格行跨卡对齐」就靠它：

```css
.grid  { display: grid; grid-template-columns: repeat(3, 1fr); }
.card  { display: grid; grid-template-rows: subgrid; grid-row: span 3; }
/* 卡片内部的标题/正文/按钮三行，与父网格行列严格对齐——
   不用 subgrid 就得硬编码行高，字体一换就错位 */
```

## 十四、T3 三件套：纯 CSS 手风琴 / 开关 / 步骤条

总纲 T3 要求「仅 CSS」实现三个组件（模态框见 13.1），这里补齐——**核心思路全一样：把状态藏进 HTML（`<details>` / 表单控件 / :target），CSS 用 `:checked` / `:open` / `:has()` 响应状态**。

### 14.1 手风琴（`<details>` 零 JS）

```html
<details class="acc" name="faq" open>          <!-- 同名 name = 互斥展开（2024 起全支持） -->
  <summary>什么是语义化？</summary>
  <p>标签选得准：h1 是标题不是"大号字"。</p>
</details>
<details class="acc" name="faq">
  <summary>Flex 和 Grid 怎么选？</summary>
  <p>一维 Flex，二维 Grid，混用很常见。</p>
</details>
```

```css
.acc { border-bottom: 1px solid #e5e5e5; }
.acc summary { padding: 14px 0; cursor: pointer; font-weight: 600;
               list-style: none; }              /* 去掉默认三角 */
.acc summary::before { content: '＋'; margin-right: 8px; }
.acc[open] summary::before { content: '－'; }
.acc p { margin: 0 0 14px; color: #555; }
```

### 14.2 切换开关（`:checked` + 兄弟选择器）

```html
<label class="switch">
  <input type="checkbox" id="dark">
  <span class="track"></span> 深色模式
</label>
```

```css
.switch { display: inline-flex; align-items: center; gap: 8px; cursor: pointer; }
.switch input { position: absolute; opacity: 0; }     /* 藏原生框但保留可聚焦/可读 */
.track { width: 44px; height: 24px; border-radius: 12px; background: #ccc;
         position: relative; transition: .25s; }
.track::after { content: ''; position: absolute; inset: 2px auto 2px 2px;
                width: 20px; border-radius: 50%; background: #fff; transition: .25s; }
.switch input:checked + .track { background: oklch(65% .2 255); }
.switch input:checked + .track::after { transform: translateX(20px); }
.switch input:focus-visible + .track { outline: 2px solid; outline-offset: 2px; }
```

### 14.3 步骤条（计数器 + 状态类）

```html
<ol class="steps">
  <li class="done">注册</li><li class="cur">填资料</li><li>完成</li>
</ol>
```

```css
.steps { display: flex; padding: 0; counter-reset: s; list-style: none; }
.steps li { flex: 1; text-align: center; position: relative; counter-increment: s; }
.steps li::before {                        /* 圆圈 + 自动编号 */
  content: counter(s);
  display: grid; place-items: center;
  width: 32px; height: 32px; margin: 0 auto 6px; border-radius: 50%;
  background: #e5e5e5; color: #888; font-weight: 700;
}
.steps li::after {                         /* 连接线 */
  content: ''; position: absolute; top: 16px; left: -50%; z-index: -1;
  width: 100%; height: 2px; background: #e5e5e5;
}
.steps li:first-child::after { display: none; }
.steps li.done::before { background: oklch(65% .2 145); content: '✓'; color: #fff; }
.steps li.done::after  { background: oklch(65% .2 145); }
.steps li.cur::before  { background: oklch(55% .2 255); color: #fff; }
```

> 💡 三个组件合起来就是「纯 CSS 交互」的全套心法：**状态在 HTML，样式靠伪类**。Tailwind 篇（04 篇 §四的 `peer-checked:` / `group-open:`）会把同一套逻辑翻译成工具类写法——两处对上号，T3 就闭环了。

## ✅ 周末 Checklist

- [ ] 用 CSS 变量替换写死的颜色
- [ ] 实现暗黑模式 + 平滑过渡 + **系统偏好检测（matchMedia）**
- [ ] 用 :has() 写过 1 次父选择器
- [ ] 写过 @keyframes 动画
- [ ] 知道 transform 比 left/top 性能好
- [ ] **T3 四件全过：纯 CSS 模态框 / 手风琴 / 开关 / 步骤条（§13.1 + §十四）**
- [ ] 知道毛玻璃怎么写
- [ ] 用过 CSS 嵌套与 subgrid 各 1 次

## 🐛 本周常见错误

| 现象 | 原因 | 解决 |
|------|------|------|
| 动画卡顿 | 用了 left/top/width 触发 layout | 改用 transform/opacity |
| transition 不生效 | 起点没值（如 display:none → block） | 用 opacity + visibility 替代 |
| transform 不生效 | 用在 inline 元素 | 改为 inline-block 或 block |
| 暗黑模式闪一下白屏 | JS 后才设置 | 头部内联脚本读 localStorage |
| backdrop-filter 没效果 | 父元素背景不透明 | 设半透明背景或祖先无 overflow |
| 动画结束后回弹 | 默认 animation-fill-mode: none | 加 `forwards` |
| animation-timeline 没反应 | Safari 不支持 / 忘了 animation-range | 用 §13.3 的 IO 兜底 |

## 📚 资源

- 动画灵感：https://animista.net
- 缓动可视化：https://easings.net
- clip-path 工具：https://bennettfeely.com/clippy
- CSS-Tricks：https://css-tricks.com
- 渐变生成：https://cssgradient.io
- 滚动驱动动画规范与示例：https://developer.chrome.com/docs/css-ui/scroll-driven-animations

下周用工具加速：Tailwind！章项目的还原工作流见第 04 篇 §十六。
