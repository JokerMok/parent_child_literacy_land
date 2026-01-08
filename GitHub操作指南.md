# Git与GitHub操作指南

## 1. 基础概念
- **仓库（Repository）**：存储代码的地方，包含所有项目文件和版本历史
- **分支（Branch）**：用于并行开发，默认主分支为 `main` 或 `master`
- **提交（Commit）**：记录代码变更的快照
- **拉取请求（Pull Request, PR）**：请求将分支合并到主分支
- **问题（Issue）**：用于追踪 bug、功能请求或讨论
- **关联仓库（Fork）**：创建他人仓库的副本到自己的GitHub账户下，用于独立开发和贡献
- **上游仓库（Upstream）**：被fork的原始仓库，用于同步最新代码
- **工作区（Working Directory）**：本地计算机上的实际文件目录
- **暂存区（Staging Area）**：临时保存将要提交的变更
- **本地仓库（Local Repository）**：存储在本地的完整版本历史
- **远程仓库（Remote Repository）**：存储在服务器上的仓库副本

## 2. Git安装与配置

### 2.1 Git安装
- **Windows**：从 https://git-scm.com/download/win 下载安装包，按照提示安装
- **macOS**：使用Homebrew安装：`brew install git`，或从官网下载安装包
- **Linux**：使用包管理器安装，如Ubuntu：`sudo apt install git`

### 2.2 Git配置
```bash
# 设置全局用户名（将出现在所有提交记录中）
git config --global user.name "你的用户名"

# 设置全局邮箱（将出现在所有提交记录中）
git config --global user.email "你的邮箱@example.com"

# 设置默认编辑器（例如VS Code）
git config --global core.editor "code --wait"

# 开启彩色输出
git config --global color.ui true

# 查看当前配置
git config --list
```

## 3. Git核心操作

### 3.1 初始化本地仓库
```bash
# 在当前目录初始化Git仓库
git init

# 在指定目录初始化Git仓库
git init 目录名
```

### 3.2 文件状态管理
```bash
# 查看文件状态
git status

# 查看文件变更内容
git diff

# 查看暂存区与最后一次提交的差异
git diff --staged
```

### 3.3 添加和提交文件
```bash
# 添加单个文件到暂存区
git add 文件名

# 添加多个文件到暂存区
git add 文件1 文件2

# 添加当前目录所有文件到暂存区
git add .

# 添加指定目录所有文件到暂存区
git add 目录名/

# 提交暂存区的文件
git commit -m "提交信息"

# 跳过暂存区，直接提交已跟踪的文件
git commit -a -m "提交信息"

# 修改最后一次提交信息
git commit --amend -m "新的提交信息"
```

### 3.4 分支管理
```bash
# 查看本地分支
git branch

# 查看所有分支（包括远程）
git branch -a

# 创建新分支
git branch 分支名

# 创建并切换到新分支
git checkout -b 分支名

# 删除本地分支（需先切换到其他分支）
git branch -d 分支名

# 强制删除本地分支
git branch -D 分支名

# 重命名本地分支
git branch -m 旧分支名 新分支名
```

### 3.5 合并分支
```bash
# 将指定分支合并到当前分支
git merge 分支名

# 合并分支时产生一个新的提交（即使是快进合并）
git merge --no-ff 分支名
```

### 3.6 远程仓库操作
```bash
# 克隆远程仓库
git clone 远程仓库地址

# 查看远程仓库
git remote -v

# 添加远程仓库
git remote add 远程仓库名 远程仓库地址

# 重命名远程仓库
git remote rename 旧仓库名 新仓库名

# 删除远程仓库
git remote remove 远程仓库名

# 从远程仓库拉取代码
git pull 远程仓库名 分支名

# 推送本地分支到远程仓库
git push 远程仓库名 分支名

# 推送本地分支并设置上游分支
git push -u 远程仓库名 分支名

# 删除远程分支
git push 远程仓库名 --delete 分支名
```

## 4. 基本操作流程

### 4.1 创建仓库
1. 登录 GitHub
2. 点击右上角 `+` 号，选择 `New repository`
3. 填写仓库名称、描述，选择公开/私有
4. 可选：初始化 README、.gitignore 和许可证
5. 点击 `Create repository`

### 4.2 Fork仓库（关联仓库）
1. 进入目标仓库的GitHub页面
2. 点击右上角的 `Fork` 按钮
3. 在弹出的页面中选择要保存到的GitHub账户
4. 等待GitHub完成fork操作
5. fork完成后，你将跳转到自己账户下的该仓库副本页面

### 4.3 克隆仓库到本地
```bash
# 克隆自己fork的仓库
git clone https://github.com/你的用户名/仓库名.git
cd 仓库名

# 添加上游仓库（原始仓库）地址
git remote add upstream https://github.com/原始仓库所有者/仓库名.git

# 验证远程仓库配置
git remote -v
```

### 4.4 从上游仓库同步代码
```bash
# 从上游仓库拉取最新代码到本地
# 首先确保当前在主分支
git checkout main
# 拉取上游仓库主分支的最新代码
git pull upstream main
# 将同步的代码推送到自己的远程仓库
git push origin main
```

### 4.5 创建和切换分支
```bash
# 创建新分支
git checkout -b 分支名

# 切换到已有分支
git checkout 分支名
```

### 4.6 提交代码
```bash
# 查看状态
git status

# 添加所有变更到暂存区
git add .

# 提交变更
git commit -m "提交信息"

# 推送到远程仓库
git push origin 分支名
```

### 4.7 创建拉取请求
1. 进入自己GitHub账户下的仓库页面
2. 点击 `Compare & pull request`
3. 在 `base repository` 下拉菜单中选择原始仓库
4. 填写 PR 标题和描述
5. 点击 `Create pull request`

### 4.8 合并拉取请求
1. 进入 PR 页面
2. 点击 `Merge pull request`
3. 确认合并

### 4.9 更新本地仓库
```bash
# 切换到主分支
git checkout main

# 拉取自己远程仓库的最新代码
git pull origin main
```

## 5. 高级操作

### 5.1 解决冲突
当合并分支遇到冲突时：
1. 查看冲突文件：`git status`
2. 编辑冲突文件，手动解决冲突
3. 标记冲突已解决：`git add 冲突文件`
4. 提交：`git commit -m "Resolve conflicts"`

### 5.2 撤销操作
```bash
# 撤销最后一次提交（保留更改）
git reset HEAD~1

# 撤销最后一次提交（丢弃更改）
git reset --hard HEAD~1

# 撤销工作区的更改
git checkout -- 文件名
```

### 5.3 标签管理
```bash
# 创建标签
git tag v1.0.0

# 推送标签到远程
git push origin v1.0.0
```

### 5.4 切换到特定提交

#### 5.4.1 查看提交历史
```bash
# 查看简洁的提交历史（单行显示）
git log --oneline

# 查看详细的提交历史
git log

# 查看最近N次提交
git log -n 5
```

#### 5.4.2 切换到特定提交（分离头指针状态）
```bash
# 复制想要切换到的提交哈希值（例如：a1b2c3d）
git checkout a1b2c3d

# 查看当前处于哪个提交
git log --oneline -n 1
```

#### 5.4.3 从特定提交创建分支
```bash
# 从特定提交创建并切换到新分支
git checkout -b 新分支名 a1b2c3d

# 或者先切换到特定提交，再创建分支
git checkout a1b2c3d
git checkout -b 新分支名
```

#### 5.4.4 直接克隆特定提交
```bash
# 克隆仓库的特定提交
git clone https://github.com/用户名/仓库名.git
cd 仓库名
git checkout a1b2c3d

# 或者使用--branch参数克隆特定提交（需要指定提交哈希）
git clone https://github.com/用户名/仓库名.git --branch a1b2c3d --single-branch
```

#### 5.4.5 回到当前分支
```bash
# 查看所有分支
git branch -a

# 切换回主分支
git checkout main
```

## 6. GitHub 协作最佳实践
- 每个功能开发创建独立分支
- 提交信息要清晰、描述性
- PR 描述要详细说明变更内容
- 定期从主分支合并到开发分支
- 使用 Issues 追踪任务和 bug
- 保护主分支，设置合并规则

## 7. 常用 GitHub 快捷键
- `t`：在仓库中搜索文件
- `w`：在仓库中搜索代码
- `i`：查看 issue 列表
- `p`：查看 PR 列表
- `l`：跳转到行号
- `y`：获取文件的永久链接

## 8. GitHub Actions
- 自动化 CI/CD 流程
- 在 `.github/workflows/` 目录下创建 YAML 配置文件
- 支持构建、测试、部署等自动化任务

## 9. 删除仓库文件

### 9.1 本地删除后推送（推荐）
1. 查看仓库中的文件：`ls`（Linux/macOS）或 `dir`（Windows）
2. 删除文件：
   ```bash
   # 删除指定文件并自动添加到暂存区
   git rm 文件名
   
   # 或者先删除文件，再手动添加到暂存区
   rm 文件名  # Linux/macOS
   del 文件名  # Windows
   git add 文件名
   ```
3. 提交删除：
   ```bash
   git commit -m "删除文件名"
   ```
4. 推送到远程仓库：
   ```bash
   git push origin 分支名
   ```

### 9.2 直接在GitHub网页上删除
1. 进入GitHub仓库页面
2. 找到要删除的文件，点击文件名进入文件详情页
3. 点击右上角的编辑按钮（铅笔图标）旁边的 `...` 菜单
4. 选择 `Delete file` 选项
5. 在页面底部填写提交信息
6. 点击 `Commit changes` 完成删除

## 10. GitHub Desktop
- 图形化界面，适合新手
- 下载地址：https://desktop.github.com/
- 支持 Windows 和 macOS

## 11. 特殊场景：仓库删除重建后重新上传

### 11.1 场景描述
当GitHub上的仓库被删除，重新创建了同名仓库后，本地项目文件还在，需要将本地项目重新关联并上传到新仓库。

### 11.2 操作步骤

#### 11.2.1 查看当前远程仓库配置
```bash
# 查看当前远程仓库配置
git remote -v
```

#### 11.2.2 删除旧的远程仓库关联
```bash
# 删除名为origin的远程仓库关联
git remote remove origin
```

#### 11.2.3 重新添加新的远程仓库
```bash
# 添加新的远程仓库关联（替换为你的GitHub仓库地址）
git remote add origin https://github.com/你的用户名/仓库名.git

# 验证新的远程仓库配置
git remote -v
```

#### 11.2.4 推送本地代码到新仓库
```bash
# 推送所有分支到新仓库
git push -u origin --all

# 推送所有标签到新仓库（如果有的话）
git push -u origin --tags
```

#### 11.2.5 验证推送结果
1. 打开GitHub网页，进入新创建的仓库
2. 检查是否所有本地文件都已成功上传
3. 确认分支和提交历史是否完整

### 11.3 注意事项
- 如果新仓库初始化了README、.gitignore等文件，推送时可能会遇到冲突
- 遇到冲突时，可以先拉取新仓库的代码，手动解决冲突后再推送
- 拉取冲突解决命令：
  ```bash
  # 拉取新仓库代码并合并
git pull origin main --allow-unrelated-histories
  ```

以上是 Git与GitHub 的完整操作指南，随着使用经验的积累，你可以逐步掌握更高级的功能和技巧。