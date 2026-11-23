---
title: Git 与 GitHub 入门
type: method-guide
chapter: "00"
chapter_title: 学习方法论
order: 4
duration: 4-6 小时
difficulty: ⭐⭐
prerequisites:
  - "[[02-环境配置完全指南]]"
tags: [Git, GitHub, 版本控制, SSH, PR, 协作]
prev: "[[02-环境配置完全指南]]"
next: "[[04-命令行终端基础]]"
created: 2026-06-19
updated: 2026-11-23
---

# Git 与 GitHub 入门

> 不会 Git 的程序员就像不会保存文件的作家——所有努力都可能瞬间归零。

## 🎯 本篇目标

- 能用自己的话讲清版本控制解决什么问题，以及为什么不用版本控制会panic
- 装好 Git 并配好 `user.name` / `user.email`，一次配置终身有效
- 画出并讲明白「工作区 / 暂存区 / 本地仓库 / 远程仓库」四个区域
- 熟练使用核心 10 个命令 + 后悔药 4 个命令（restore / reset / revert / reflog）
- 配好 SSH key，让 `git push` 不用反复输密码
- 用 `gh` CLI 完成人生第一个 PR
- 写出符合约定式提交规范的 commit message

---

## 一、什么是版本控制？📼

想象三个场景：

1. **打游戏存档：** 你怕 BOSS 太难，先存档，打死了再继续；打不过就读档重来。
2. **Word 撤销：** Ctrl+Z 一下回到上一秒。
3. **多人改 PPT：** 张三改一版，李四改一版，最后谁的版本是对的？

Git 解决的就是这三件事：**存档、回滚、合并多人改动**。

- **Git** = 工具本身（在你电脑上跑）
- **GitHub** = 一个网站，把你的"存档"放到云端，方便分享和协作

⚠️ Git ≠ GitHub。Gitee、GitLab 都是类似 GitHub 的网站，底层用的都是 Git。

---

## 二、Git 安装与初始配置 ⚙️

### 安装

```bash
# macOS（如果上一节装了 Xcode 工具就已经有）
brew install git

# WSL / Ubuntu
sudo apt install git
```

### 初始配置（只需做一次）

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"
git config --global init.defaultBranch main
git config --global core.editor "code --wait"   # 装了 VSCode 后再设
```

> 这个邮箱要和后面 GitHub 注册邮箱一致，否则贡献统计不显示头像。

### 验证

```bash
git config --list
```

---

## 三、四大区域模型（必须看懂）🗺️

```
┌─────────────┐  git add   ┌──────────┐  git commit  ┌──────────┐  git push   ┌──────────┐
│  工作区     │ ─────────> │ 暂存区    │ ───────────> │ 本地仓库  │ ──────────> │ 远程仓库  │
│ (你编辑文件) │            │ (Staging) │              │ (.git 目录)│            │ (GitHub)  │
└─────────────┘ <───────── └──────────┘ <─────────── └──────────┘ <────────── └──────────┘
                git restore --staged   git reset       git pull / git fetch
```

| 区域   | 含义          | 类比     |
| ---- | ----------- | ------ |
| 工作区  | 你正在改的文件     | 草稿纸    |
| 暂存区  | 准备提交的内容     | 装订夹    |
| 本地仓库 | 你机器上的存档     | 自己的存档槽 |
| 远程仓库 | GitHub 上的存档 | 云端备份   |

---

## 四、核心 10 命令场景手册 📚

### 1. `git init` —— 创建仓库

> 场景：你写了一个新项目，想用 Git 管理。

```bash
mkdir my-project && cd my-project
git init
```

会生成隐藏的 `.git` 目录（这就是仓库本体，别删）。

### 2. `git clone` —— 克隆别人的仓库

> 场景：你想要别人在 GitHub 上的项目代码。

```bash
git clone https://github.com/torvalds/linux.git
```

### 3. `git add` —— 加入暂存区

> 场景：改完文件，告诉 Git "这次提交要带上它们"。

```bash
git add README.md           # 加单个文件
git add .                   # 加全部改动
```

### 4. `git commit` —— 存档

> 场景：到了一个里程碑，存一下。

```bash
git commit -m "feat: 添加登录页面"
```

### 5. `git push` —— 推到远程

> 场景：把本地存档传到 GitHub。

```bash
git push origin main
```

### 6. `git pull` —— 拉取远程更新

> 场景：同事更新了代码，你要同步下来。

```bash
git pull origin main
```

### 7. `git branch` —— 分支管理

> 场景：你想在不影响主线的情况下试个新功能。

```bash
git branch                  # 列出所有分支
git branch feature/login    # 新建分支
git branch -d old-branch    # 删除分支
```

### 8. `git checkout` / `git switch` —— 切换分支

```bash
git switch feature/login        # 切到分支
git switch -c feature/signup    # 新建并切换
```

### 9. `git merge` —— 合并分支

> 场景：feature 分支测好了，合到 main。

```bash
git switch main
git merge feature/login
```

### 10. `git log` —— 看历史

```bash
git log --oneline --graph --all    # 漂亮的图形化历史
```

### 自我检查 ✅

```bash
mkdir git-test && cd git-test
git init
echo "hello" > a.txt
git add a.txt
git commit -m "first commit"
git log
```

看到一条提交记录就成功了。

> 👉 只会提交还不够——**下一节「后悔药」才是真正保命的**，那 4 个命令（restore / reset / revert / reflog）请务必练熟。

---

## 五、后悔药：撤销与回滚 🧯

Git 一半的价值在"后悔药"。新手的真正痛点不是不会提交，而是**提交错了不知道怎么退回来**。下面这些命令按"后悔程度"从小到大排，**这节比上一节的 10 个命令更救你命**。

### 1. `git restore` —— 丢掉工作区的改动（还没提交）

> 场景：改着改着发现方向错了，想丢掉未提交的修改。

```bash
git restore 文件名              # 丢弃某个文件的改动
git restore .                  # 丢弃所有文件的改动（不可恢复，慎用！）
```

⚠️ `git restore .` 一按就没了，**没有后悔药**。想试错就先 `git stash` 存起来。

### 2. `git restore --staged` —— 从暂存区撤回（还没 commit）

> 场景：`git add .` 一把梭，把 node_modules、.env 也塞进暂存区了。

```bash
git restore --staged 文件名      # 撤回暂存，文件内容还留在工作区
git restore --staged .          # 清空整个暂存区
```

### 3. `git reset` —— 回退提交（三个挡位）

> 场景：commit message 写错了，或者想把一个大提交拆成几个小提交。

```bash
git reset --soft HEAD~1     # 撤销提交，改动回到【暂存区】
git reset HEAD~1           # （等于 --mixed）撤销提交，改动回到【工作区】
git reset --hard HEAD~1     # 撤销提交，改动直接消失 ⚠️ 最危险
```

三个挡位的区别就一句话：**`--soft` 留在暂存区，`--mixed` 留在工作区，`--hard` 什么都不留。** `HEAD~1` 表示"上一个提交"，`HEAD~3` 就是往前数三个。

### 4. `git revert` —— 用一个新提交抵消旧提交（已推送时的安全做法）

> 场景：已经 push 到 GitHub 的提交发现有 bug，但历史不能改。

```bash
git revert <commit-hash>       # 生成一个"反向提交"抵消掉它
git revert --no-edit <hash>    # 不弹编辑器，用默认说明
```

**为什么已推送的提交要用 `revert` 而不是 `reset`？** 因为 push 过的历史是**公共的**：`reset` 会改写历史，别人 pull 时会历史分叉、冲突不断；而 `revert` 只是**多加一个提交**，所有人正常 pull 即可。

> 📌 **一句话规则：没 push 用 `reset`，已经 push 用 `revert`。**

### 5. `git reflog` —— 后悔药的最后一根稻草 🆘

前面所有命令都是"撤销"，`reflog` 是"**找回**"。它记录了 HEAD 每一次移动的位置，哪怕你 `reset --hard` 之后也能回到那个点。

```bash
git reflog                  # 看 HEAD 的移动历史
git reset --hard HEAD@{3}   # 回到 3 步之前的状态
```

⚠️ 两条限制：`reflog` 只在**本地**保留约 90 天，而且只对本地分支有效。**它不是备份**——该 push 还是 push。

### 自我检查 ✅

```bash
mkdir git-undo && cd git-undo
git init
echo "hello" > a.txt
git add a.txt && git commit -m "first commit"

echo "bad" >> a.txt           # 改坏
git restore a.txt             # 撤销工作区改动
git status                    # 应该干净了

git log --oneline             # 看看历史
git reflog                    # 看看 HEAD 走过哪些地方
```

---

## 六、GitHub 注册 + SSH key 配置 🔐

### 1. 注册 GitHub

去 [github.com](https://github.com) 注册，邮箱用之前 git config 设的那个。

### 2. 生成 SSH key

**什么是 SSH key？** 一对密钥（公钥 + 私钥）。把公钥告诉 GitHub，以后传代码就不用每次输密码了。

```bash
ssh-keygen -t ed25519 -C "你的邮箱@example.com"
```

一路回车（密码留空就行）。

### 3. 上传公钥到 GitHub

```bash
cat ~/.ssh/id_ed25519.pub
```

复制输出（以 `ssh-ed25519` 开头）。

打开 GitHub → Settings → SSH and GPG keys → New SSH key → 粘贴 → Save。

### 4. 测试

```bash
ssh -T git@github.com
```

看到 `Hi xxx! You've successfully authenticated.` 就成功了。

### 5. 装 gh CLI（GitHub 官方命令行）

```bash
# macOS
brew install gh

# WSL / Ubuntu 24.04 (noble) 及更新
sudo apt install gh

# 登录
gh auth login
```

之后可以 `gh repo create`、`gh pr create` 等。

> ⚠️ **Ubuntu 22.04 (jammy) 的坑**：`sudo apt install gh` 在 jammy 上只能装到 **2.4.0**（2021 年的版本，`gh pr create --fill`、`gh repo create --public` 等新特性会缺）。两个办法：
> 1. **升级系统**（推荐）：`sudo do-release-upgrade` 升到 24.04 LTS（noble），那里的包是 2.45.0+。
> 2. **用官方源装新版**：
>    ```bash
>    sudo mkdir -p /etc/apt/keyrings
>    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null
>    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list
>    sudo apt update && sudo apt install gh
>    ```
>
> 装完检查：`gh --version`（当前最新 v2.105.0）。

---

## 七、第一个 PR 实战 🎯

PR = Pull Request = "请把我的改动合并到你的项目里"。开源协作的标准动作。

### 流程

```
你 fork → 你 clone → 改代码 → 你 push → 在 GitHub 上发起 PR → 项目作者审核合并
```

### 步骤

1. 在 GitHub 找一个项目，点右上角 **Fork**（复制一份到你账号下）
2. clone 你 fork 后的仓库：
   ```bash
   git clone git@github.com:你的用户名/项目名.git
   cd 项目名
   ```
3. 新建分支：
   ```bash
   git switch -c fix/typo
   ```
4. 改文件，比如修一个错别字
5. 提交：
   ```bash
   git add .
   git commit -m "docs: 修正 README 错别字"
   git push origin fix/typo
   ```
6. 用 gh 一键开 PR：
   ```bash
   gh pr create --fill
   ```

🎉 你已经迈出了开源贡献第一步！

> 🎯 **第一次 PR 不知道该改哪个仓库？** 用 [firstcontributions/first-contributions](https://github.com/firstcontributions/first-contributions)（⭐ ~57k，专门为新手练手而建，每天都有人提 PR）。它的 README 里有一份"Add your name" 的任务清单，照着做即可，不会被 maintainer 拒绝。
>
> 💡 另一个经典靶子是 [octocat/Spoon-Knife](https://github.com/octocat/Spoon-Knife)（⭐ ~14k，GitHub 官方专门用来练手的 fork 练习仓库，fork 数已超 16 万）。

---

## 八、约定式提交规范 ✍️

让你的提交信息一眼能看懂：

```
<类型>(<范围>): <简短描述>

[可选的详细说明]
```

| 类型 | 含义 | 例子 |
|------|------|------|
| feat | 新功能 | `feat(auth): 添加微信登录` |
| fix | 修 bug | `fix(api): 修正空指针` |
| docs | 文档 | `docs: 更新 README` |
| style | 格式（不影响逻辑） | `style: 统一缩进` |
| refactor | 重构 | `refactor: 抽取工具函数` |
| test | 测试 | `test: 添加登录用例` |
| chore | 杂项 | `chore: 升级依赖` |

---

## 九、🐛 常见错误 🚨

先查速查表，再往下看细节。

| 错误现象 | 原因 | 解决 |
|---|---|---|
| `Please tell me who you are` | Git 不知道你是谁 | `git config --global user.name "你的名字"` + `git config --global user.email "邮箱"` |
| `error: The following untracked working tree files would be overwritten by merge` | 本地有未提交的新文件，和要拉下来的文件重名 | 先 `git add` + `commit` 你的改动，或 `git stash` 暂存后再 pull |
| `! [rejected] main -> main (fetch first)` | 远端比你新 | `git pull --rebase`（个人分支）或 `git pull`（有冲突时手动解） |
| `CONFLICT (content): Merge conflict in xxx` | 同一行被两个人改过 | 打开冲突文件删掉 `<<<<<<< / ======= / >>>>>>>` 三段标记，保留正确内容后 `git add` |
| `fatal: not a git repository` | 当前目录不是仓库 | `cd` 到仓库目录，或 `git init` |
| `detached HEAD` | 切到了某个 commit 而不是分支 | `git switch main` 回到主分支；要保留改动先 `git switch -c 新分支名` |
| `Permission denied (publickey)` | SSH key 没配好或没上传 | `ssh -T git@github.com` 验证；重新 `cat ~/.ssh/id_ed25519.pub` 贴到 GitHub |
| `gh: command not found` | 没装 gh CLI | 见「六、GitHub 注册 + SSH key 配置」第 5 步 |
| `gh auth login` 后仍提示未登录 | token 没写进 keychain | 重新 `gh auth login` 选 HTTPS；用 `gh auth status` 检查 |
| 不小心 commit 了密钥 / 密码 | 忘了先写 `.gitignore` | **先去服务商重置密钥**，再按下面「不小心 commit 了密钥/密码」处理历史 |
| 改了文件但 `git status` 说没变化 | `.gitignore` 把它忽略了，或行尾符差异（Windows CRLF） | `git check-ignore -v 文件名` 看是否被忽略；行尾问题见 [[05-VSCode与AI辅助编程]] |
| `git push` 提示要密码 / 2FA | 用了 HTTPS 而不是 SSH | 配好 SSH key 后改用 `git@github.com:...` 形式的 remote 地址 |

### merge conflict（合并冲突）

```
CONFLICT (content): Merge conflict in xxx.txt
```

打开冲突文件，会看到：

```
<<<<<<< HEAD
你的版本
=======
对方的版本
>>>>>>> branch-name
```

手动选择保留哪部分，删掉 `<<<<<<<` `=======` `>>>>>>>` 这些标记，然后：

```bash
git add xxx.txt
git commit
```

### detached HEAD（游离状态）

意思是你切到了某个具体的 commit，不在任何分支上。修了东西也保不下来。

**解决：**

```bash
git switch -c temp-branch    # 创建分支保住改动
```

### `! [rejected] main -> main (fetch first)`

**原因：** 远程有你本地没有的提交。

**解决：**

```bash
git pull --rebase origin main
git push origin main
```

### 不小心 commit 了密钥/密码

⚠️ **第一件事不是删 commit，而是去服务商重置那个密钥。** 只要有人 clone 过，你的密钥就当**已经泄露**了——删文件删不掉历史。

**还没 push：**

```bash
# 1️⃣ 立刻去服务商后台重置密钥（AWS / OpenAI / GitHub Token / 数据库密码……）
# 2️⃣ 撤销这次提交，改动还在（--soft），先把它挡在 .gitignore 后面再提交
git reset --soft HEAD~1
echo ".env" >> .gitignore
git add .gitignore
git commit -m "chore: 忽略 .env"
```

**已经 push 了：**

```bash
# 用一个新提交抵消掉（最稳，别人 pull 不会冲突）
git revert <那个提交的 hash>
git push origin main
```

但要清楚：`revert` **不会**把密钥从历史记录里真正抹掉，它只是在新版本里不再包含这个文件。公开仓库要彻底清理得用 `git filter-repo` 或 BFG 重写历史（操作复杂、风险高，**新手慎用**）。

> 📌 **所以真正的正确做法永远是第 1 步：重置密钥。** 清历史是补救手段，不是保险丝。

---

## 我学完了吗？✅ checklist

- [ ] 能讲清楚 工作区/暂存区/本地仓库/远程仓库 四个区域
- [ ] 会用 init / add / commit / push / pull
- [ ] 会建分支并合并
- [ ] 配好了 SSH key，能免密 push
- [ ] 装了 gh CLI 并 `gh auth login`
- [ ] 完成了人生第一个 PR
- [ ] 提交信息会用约定式规范
- [ ] 会用 restore / reset / revert / reflog 撤销与回滚
- [ ] 遇到 merge conflict 不慌

全部打勾 → 进入下一篇《命令行终端基础》🚀

---

## 📚 参考与延伸阅读

- 📘 [Pro Git 中文版](https://git-scm.com/book/zh/v2)——Git 官方教材，四个区域模型的出处
- ↩️ [Undoing Things（英文）](https://git-scm.com/book/en/v2/Git-Basics-Undoing-Things)——「后悔药」的官方章节
- 🔧 [git reset 官方文档](https://git-scm.com/docs/git-reset) / [git restore](https://git-scm.com/docs/git-restore) / [git revert](https://git-scm.com/docs/git-revert) / [git reflog](https://git-scm.com/docs/git-reflog)——四个命令的精确语义
- 🔀 [Learn Git Branching](https://learngitbranching.js.org/?locale=zh_CN)——把分支和合并当游戏玩一遍
- 🔐 [GitHub 官方文档 · 用 SSH 连接](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh)——SSH 配置步骤
- 🧑‍💻 [gh CLI 手册 · gh pr create](https://cli.github.com/manual/gh_pr_create) / [gh auth login](https://cli.github.com/manual/gh_auth_login)——命令行提 PR 与登录
- 🎯 [如何创建一个 Pull Request](https://docs.github.com/zh/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)——GitHub 官方 PR 指南
- 🔍 [GitHub 代码搜索](https://docs.github.com/zh/search-github/github-code-search)——看懂高级搜索语法
- ✍️ [约定式提交规范（中文）](https://conventionalcommits.org/zh-hans/)——commit message 的行业标准
- 🤝 [Open Source Guides · How to Contribute](https://opensource.guide/how-to-contribute/) / [Good First Issue](https://goodfirstissue.dev/)——去哪找可以练手的 issue
- 🎮 [firstcontributions/first-contributions](https://github.com/firstcontributions/first-contributions)——专为新手设计的第一个 PR 靶子
