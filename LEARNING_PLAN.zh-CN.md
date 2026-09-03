# Code-Fixer 一周看懂源码 · 学习计划

> 目标：一周后能独立讲清 Code-Fixer 运行链路，能改配置、加工具、读轨迹，为简历和二次开发打底。
> 前提：已能跑通快速开始（deepseek-v4-pro + 本地 docker 沙箱）。
> 建议每天 2~3 小时；先"自上而下"理解主线，再抠细节。

---

## 主线地图（先记住这张图）

```
CLI 入口 (run.py)
   │
   ├─ SWEEnv (environment/swe_env.py)  ← 薄封装 SWE-ReX
   │     └─ SWE-ReX Deployment → Docker/modal/aws 容器
   │           └─ 容器内 shell session + ACI 自定义工具
   │
   └─ Agent (agent/agents.py)  forward() 主循环
         ├─ HistoryProcessor (agent/history_processors.py)  压缩上下文
         ├─ 模型调用 (agent/models.py, litellm)
         ├─ Parser (tools/parsing.py)  解析模型输出 → 动作
         └─ 动作经 SWEEnv → 容器 Shell 执行 → 观察回填
```

一条命令跑起来时，代码路径大致是：
`run.py → run_single.run_from_config → RunSingle.from_config().run() → env.start() + agent.run()`

---

## Day 1 · 总览 + 架构 + 跑通对照
**目标**：建立全局观，能把一条命令对应到代码各阶段。
- 读 `docs/background/architecture.md`、`docs/index.md`
- 通读目录树：`codefixer/` 下 `run/ agent/ environment/ tools/ utils/`
- 看 `pyproject.toml`（入口、依赖），`codefixer/run/run.py`（118 行，很薄）
- 实操：再跑一次快速开始，把日志的每个阶段（Starting environment → Runtime started → Uploading → Running agent → Submission）和架构图对上号
**产出**：画一张自己的架构流程图（文字版即可）。

## Day 2 · 配置系统 + CLI
**目标**：明白"一个 yaml + 一堆 `--key=value`"如何变成一个配置对象。
- 读 `run/run.py`、`run/run_single.py`（189 行）、`types.py`（82 行）
- 读 `config/default.yaml` 与 `config/local_deepseek.yaml`，逐字段理解
- 读 `utils/config.py`（64 行，看配置怎么加载/合并）
- 跟踪一个参数：`--env.deployment.image` 从 CLI 一路到 EnvironmentConfig 对应字段
**产出**：能用一句话解释 `problem_statement / agent / env` 三段配置各管什么。

## Day 3 · 环境层 SWEEnv + SWE-ReX + 仓库
**目标**：理解"沙箱到底怎么搭起来"。
- 读 `environment/swe_env.py`（242 行）、`environment/repo.py`（207 行）
- 理解 SWE-ReX Deployment：`docker run --rm -p 端口:8000 ... python:3.12 /bin/sh -c 'swerex-remote --auth-token ...'`
- 弄清 `env.repo.github_url` vs `env.repo.path` 的差异，以及仓库如何被打包上传进容器
**产出**：能讲清"环境初始化"的 4 步（拉镜像→起容器→装 swerex-remote→上传仓库）。

## Day 4 · Agent 主循环（最核心）
**目标**：吃透 `forward()` 这一轮循环。
- 精读 `agent/agents.py`（1119 行，最大文件；重点 `forward`、`add_step_to_history`、`submit` 判定、`_step`）
- 读 `agent/models.py`（783 行，看 litellm 如何调用 openai/deepseek）
- 理解循环：SYSTEM → 模型 → parser 提取命令 → SWEEnv 执行 → observation → 下一轮
**产出**：画出 agent 单轮完整流程图，解释 `THOUGHT`+bash 如何被解析并执行。

## Day 5 · 工具 + 输出解析
**目标**：明白"模型一句话为何能改文件/跑测试"。
- 读 `tools/tools.py`（366 行）、`tools/commands.py`（183 行）、`tools/bundle.py`（43）、`tools/submit`
- 读 `tools/parsing.py`（517 行）：`single_bash_code_block` / `thought_action` 解析器
- 理解 ACI 工具注入容器、bash 工具、`submit` 如何产出最终 patch
**产出**：亲自加一个自定义工具（如 `read_file`），记录改动步骤。

## Day 6 · 问题来源 + 历史压缩 + 批量评测
**目标**：理解"任务从哪来 + 上下文怎么省 + 批量怎么跑"。
- 读 `agent/problem_statement.py`（235 行）：github issue / file / text / swebench 四种来源
- 读 `agent/history_processors.py`（317 行）：上下文压缩（cache_control、去掉它等）
- 读 `run/run_batch.py`（392 行）、`run/batch_instances.py`（366 行）：SWE-bench 批量与评测
**产出**：能解释 SWE-bench / mini-swe-agent 数据来源与指标（x% 解决率）。

## Day 7 · 轨迹深读 + 测评 + 成果产出
**目标**：把看懂的东西变成"能讲、能写"。
- 打开之前生成的 `.traj`（`trajectories/oo/.../d48f76/d48f76.traj`），逐段读模型输入/输出/命令，对照 Day4 循环
- 扫读 `tests/`，了解单元/集成测试怎么覆盖核心逻辑
- 整理成果：写一篇 500 字「Code-Fixer 运行原理」总结 + 一张架构图
**产出**：一份可直接放进简历/面试讲稿的项目说明（技术栈、原理、你的工作、量化结果）。

---

## 学习方法提醒
- **先主线后细节**：每章先看入口和主流程，再深入局部；别一上来扣 parser 细节。
- **代码 + 日志对照**：跑一次任务，边看输出边定位代码行，理解最快。
- **善用 `--help_option`**：`codefixer run --help_option codefixer.environment.swe_env.EnvironmentConfig` 能列出某段配置的所有字段。
- **遇到看不懂先放过**：`models.py`/`reviewer.py`/`inspector` 可后看，不影响主线。

## 可选的 Day 8+（进阶，按需）
- 加装 tools / 自定义 ACI
- 用 `run-batch` 跑 `swe_bench lite` 拿量化成绩
- 对比 `mini-swe-agent`（官方新方向，用 100 行 Python 实现）