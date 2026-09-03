# Code-Fixer 快速开始（本机实测可跑通）

> 环境：Windows + PowerShell / DeepSeek v4-pro（OpenAI 兼容）/ Docker 本地沙箱
> 已验证：`deepseek-v4-pro` 成功修复 `demo_repo/app.py` 的 bug，生成 patch ✅

---

## 0. 前置条件（已配好）

- Code-Fixer 1.1.0 装在 `.venv`（`code-fixer\.venv\Scripts\codefixer.exe`）
- 模型 API Key 已写入**环境变量**：`DEEPSEEK_API_KEY`
- Docker 可用，且本地已拉好镜像 **`python:3.12`**（重要，见「踩坑 1」）
- Git 已配代理 `http://127.0.0.1:8902`（但 Code-Fixer 的 GitHub 请求不读它，见「踩坑 2」）

---

## 1. 模型配置

使用仓库自带配置 `config/local_deepseek.yaml`，关键内容：

```yaml
agent:
  model:
    name: openai/deepseek-v4-pro
    api_base: https://api.deepseek.com/v1
    api_key: $DEEPSEEK_API_KEY      # 自动读环境变量
    per_instance_cost_limit: 0      # 关闭成本限制
    per_instance_call_limit: 50
    total_cost_limit: 0
  tools:
    parse_function:
      type: single_bash_code_block  # 模型用 bash 代码块输出动作
```

---

## 2. 准备一个测试仓库

用本地目录作为 agent 要修改的仓库（`demo_repo`）：

```powershell
# 目录里有 app.py + run_tests.py + .git 即可
D:\Development\Project\PythonAgentProject\demo_repo
```

再写一个**问题描述文件**（`demo_problem.md`）：

```markdown
修复这个仓库的 bug：max_of 在传入空列表时应返回 None，而不是抛出 IndexError；
请只修改 app.py，不要改测试文件。
```

---

## 3. 运行（本地仓库方式，推荐）

```powershell
$env:PYTHONUTF8 = '1'
Set-Location D:\Development\Project\PythonAgentProject\code-fixer

& '.\.venv\Scripts\codefixer.exe' run `
  --config config/local_deepseek.yaml `
  --env.deployment.image=python:3.12 `
  --env.repo.path=D:\Development\Project\PythonAgentProject\demo_repo `
  --problem_statement.path=D:\Development\Project\PythonAgentProject\demo_problem.md
```

运行过程：拉容器 → 上传 demo_repo → agent 反复「思考+敲命令」→ 修改代码 → 跑测试 → `submit`。

---

## 4. 结果产物

成功后自动生成（在 `code-fixer\trajectories\...`）：

- `*.patch` —— 修复补丁（可 `git apply` 应用）
- `*.traj` —— 完整运行轨迹（每一步模型输入/输出/命令）

本次成功补丁：

```diff
diff --git a/app.py b/app.py
--- a/app.py
+++ b/app.py
@@ -1,6 +1,8 @@
 def max_of(nums):
     """Return the largest number in nums, or None if the list is empty."""
-    m = nums[0]  # BUG: IndexError when nums is empty
+    if not nums:
+        return None
+    m = nums[0]
     for n in nums[1:]:
         if n > m:
             m = n
```

---

## 5. 踩坑记录（务必看）

### 踩坑 1：`docker pull python:3.11` 超时
Code-Fixer 默认要 `python:3.11`，但本机连 Docker Hub 超时（网络问题）。
**解决**：用 `--env.deployment.image=python:3.12` 指定本地已有镜像。

### 踩坑 2：官方 GitHub issue 版跑不通
官方教程用：

```powershell
codefixer run --config config/default.yaml `
  --env.repo.github_url=https://github.com/SWE-agent/test-repo `
  --problem_statement.github_url=https://github.com/SWE-agent/test-repo/issues/1
```

会报 `SSL EOF`，因为：
- 直连 `api.github.com` 被网络阻断；
- 无 `GITHUB_TOKEN`；
- Code-Fixer 的 GitHub 请求走 Python urllib，**不读** `git config` 里的 8902 代理。

**解决**（任选其一，才能跑官方版）：
- 配置 `GITHUB_TOKEN` 环境变量；或
- 给 Code-Fixer 设代理：`$env:HTTPS_PROXY='http://127.0.0.1:8902'`（注意会影响所有请求）。