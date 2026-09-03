# Code-Fixer 学习计划（看懂版 · 纯阅读，不改动代码）

> 目标：把 Code-Fixer 的运行链路**看懂、能讲**（为简历和面试），不修改任何代码。
> 方式：Python 速成 1 天（对照 Java）→ 源码精读（**先大脑后手脚**）→ 日志/轨迹/测试对照。
> 顺序说明：Agent 主循环（大脑）优先；环境层（手脚/管道）降级为 D6 补充阅读，先以"打电话"的功能理解即可。
> 时间：10 个学习日 × 每天 2~3 小时 ≈ 20~30 小时（约 2 周，含缓冲）。
> 注：D1 是压缩的"Week 1"，内容偏多，可拆成两个半天，或只做前半（后半"跑通对照"你已有成功记录，直接看日志即可）。

---

## 主线地图（先记住这张图，每天对照它）

```
CLI 入口 (codefixer run → run/run.py)
   │
   ├─ SWEEnv (environment/swe_env.py)  ← 薄封装 SWE-ReX（Docker 沙箱）
   │     └─ SWE-ReX Deployment → docker run → 容器内 shell session + ACI 工具
   │
   └─ Agent (agent/agents.py)  forward() 主循环
         ├─ HistoryProcessor (agent/history_processors.py)   压缩上下文
         ├─ 模型调用 (agent/models.py, litellm)              LLM 对话
         ├─ Parser (tools/parsing.py)                        模型输出 → 动作
         └─ 动作经 SWEEnv → 容器 Shell 执行 → observation 回填 → 下一轮
```

一条命令的代码路径：`run.py → run_single.run_from_config → RunSingle.from_config().run() → env.start() + agent.run()`

---

## 第 0 天 · Week 1 精简版：Python 速成 + 生态 + 项目总览（D1，1 天）✅ 已完成（笔记：`DAY1_NOTES.zh-CN.md`）

> 你是 Java 精通，这一天只做"语法翻译 + 认门"，不学编程本身。

**前半 · Python 速成（对照 Java，用文末速查表）**
- 语法：动态类型、list/dict/set/tuple（对照 `List<T>`/`Map<K,V>`）、切片、`for x in xs` + `enumerate`、f-string、`*args/**kwargs`
- OOP 与进阶：`class`/`self`（对照 `this`）、`@dataclass`（对照 record）、`@property`、装饰器 `@`（对照注解+AOP）、`with`（对照 try-with-resources）、`try/except`、类型注解（不强制）、推导式（对照 Stream）、`yield`
- 练习：读 `demo_repo/app.py`（你之前修过 bug 的那个文件），逐行翻译成 Java 逻辑

**中段 · Python 工程生态（对照 Maven/JUnit）**
- `pyproject.toml`（对照 pom.xml）：重点看 `[project.scripts]` 入口 `codefixer = "codefixer.run.run:main"`、依赖列表（litellm / swe-rex / pydantic…）
- `uv`/`.venv`（对照依赖管理）、`pytest`（对照 JUnit，看 `[tool.pytest.ini_options]`）、`ruff`（对照 Checkstyle）

**后半 · 项目总览 + 跑通对照**
- 读 `docs/background/architecture.md`、`docs/background/aci.md`
- 通读目录树：`codefixer/` 下 `run/ agent/ environment/ tools/ utils/` 各包职责
- 对照：你已有成功运行记录（`run_demo_v4.log` 等 + `QUICKSTART.zh-CN.md`），把日志每个阶段（Starting environment → Runtime started → Uploading → Running agent → Submission）和架构图对上号，**不需要重跑**
- 产出：能读懂 Python 代码 + 知道入口/结构/测试方式 + 画一张架构流程图

---

## 第一部分 · 源码主线精读（先大脑后手脚，D2–D6）

**D2 · Agent 主循环 `forward()`（最核心，2~3h）✅ 已完成**
- 精读：`agent/agents.py`（1119 行，全项目最大文件）——重点：`forward`、`_step`、`add_step_to_history`、`submit` 判定
- 理解循环：SYSTEM 提示 → 模型调用 → parser 提取命令 → SWEEnv 执行 → observation 回填 → 下一轮；什么时候停止（`submit`/次数上限）
- 环境层只需功能理解：`env.communicate(命令)` = "打电话让沙箱执行命令并返回输出"，细节 D6 再补
- 产出：画出 agent 单轮完整流程图，能解释 `THOUGHT` + bash 代码块如何被解析并执行

**D3 · 模型层 + 历史压缩（2~3h）**
- 读：`agent/models.py`（783 行）——litellm 如何调用 `openai/deepseek-v4-pro`，看 `--config` 里 `api_base`/`api_key`/`per_instance_call_limit` 对应代码哪里
- 读：`agent/history_processors.py`（317 行）——上下文压缩策略（为什么长任务不爆 context window）
- 产出：能解释"为什么 API Key 写在环境变量里也能被读到"

**D4 · 工具系统 + 输出解析（2~3h）**
- 读：`tools/tools.py`（366 行）、`tools/commands.py`（183 行）、`tools/parsing.py`（517 行）
- 理解：ACI 工具如何注入容器 shell；`single_bash_code_block` / `thought_action` 解析器；`submit` 如何产出最终 `*.patch`
- 产出：能解释"模型一句话为什么能改文件/跑测试/提交 patch"

**D5 · 问题来源 + 批量评测 + SWE-bench（2~3h）**
- 读：`agent/problem_statement.py`（235 行）——github issue / file / text / swebench 四种任务来源
- 读：`run/run_batch.py`（392 行）、`run/batch_instances.py`（366 行）——批量跑分与评测逻辑
- 了解：SWE-bench 是什么（真实 GitHub issue 数据集）、`x% 解决率` 怎么算（生成 patch → 跑官方测试 → 是否通过）
- 产出：能解释"SWE-bench verified 65% 解决率"这句话的含义

**D6 · 环境层补充阅读（可选深入，1~2h）**
> 主线已通，环境层按需补细节；读不懂的部分用"打电话"比喻理解即可，不影响主线。
- 读：`environment/swe_env.py`（242 行）、`environment/repo.py`（207 行）
- 重点看：`communicate()`（命令进出）、`start()` 的 4 步（起容器→建会话→传代码→复位）、仓库三兄弟（`type` 判别字段：local=zip 上传 / github=容器内 clone / preexisting=不搬）
- 对照日志：`Starting container ... python:3.12` / `Uploading file from ... demo_repo` / `Resetting repository ... HEAD`
- 产出：能讲清"环境初始化 4 步"，那行 `docker run` 命令的来源

**✅ 第一部分检查点**：能不看代码讲出完整主线（大脑优先），能指出任意一步对应哪个文件哪段逻辑

---

## 第二部分 · 巩固理解（纯观察，D7–D10）

**D7 · 轨迹深读（2~3h）**
- 打开之前生成的 `.traj`（`trajectories/oo/.../*.traj`），逐段读：系统提示 → 模型思考 → 命令 → 输出 → 下一轮，对照 D2 的循环图
- 顺便对照日志 `run_demo_v4.log` / `run_hello_world.log` 里的每个阶段输出
- 产出：能给别人讲解一份轨迹，"agent 是怎么一步步修好 bug 的"

**D8 · 测试套件通读（2~3h）**
- 扫读 `tests/`（31 个文件、约 1900 行），重点看核心逻辑的测试怎么组织：`test_parsing`、`test_agents`、`test_env`、`test_config` 等
- 用测试反推理解：parser 接受什么格式、agent 停止条件、配置合并行为
- 产出：能说"这些行为是由哪些测试保证的"（对照你 JUnit 测试的阅读经验）

**D9 · 批量评测机制理解（2~3h）**
- 精读 `run/run_batch.py` 的主流程，理解单条任务如何被并行调度、结果如何汇总
- 理解 `submit` 产物（`*.patch`）与评测的关系：patch → 官方测试 → 通过/失败
- 可选观察（不改代码）：用已有配置只跑 1 个 demo 问题，观察批量入口的输出格式
- 产出：能讲清"SWE-bench 评测的完整闭环"：任务 → agent → patch → 测试 → 分数

**D10 · 生态对比 + 主线复述（1~2h）**
- 了解官方新方向 `mini-swe-agent`（100 行 Python 实现同性能）——面试加分项，"我知道生态走向"
- 闭卷复述主线地图：从 CLI 讲到 patch 生成；卡壳的地方回到对应代码再看一遍
- 产出：能对着白板（或空文档）完整讲一遍 Code-Fixer 的运行原理

**✅ 第二部分检查点**：能讲解一份真实轨迹、能讲清评测闭环、能脱稿复述主线

---

## 简历素材清单（看懂版 · 做完即拥有）

1. **源码精读**：能讲清 Agent 主循环 / 工具系统 / 配置系统 / SWE-ReX 环境层（对应文件、行数级理解）
2. **链路理解**：从 CLI 到 patch 生成的完整运行链路 + 单轮循环流程图
3. **轨迹分析**：能解读真实 `.traj`，讲清 agent 每一步的思考与行动
4. **评测理解**：能解释 SWE-bench / 解决率指标的含义与计算方式
5. **生态认知**：Code-Fixer vs mini-swe-agent 的对比观点

> 简历写法建议：写"**深入理解并讲解 Code-Fixer 架构：Agent 主循环、工具系统、SWE-ReX 沙箱环境与评测链路**"，附上你能讲清楚的具体模块。

---

## 面试高频问题（对应本计划内容）

1. 什么是 ACI（Agent-Computer Interface）？和普通的 function calling / tool use 有什么区别？
2. 一句话说清 Code-Fixer 的运行流程（CLI → 环境 → Agent 循环 → patch）
3. 为什么用 Docker 沙箱跑 agent？安全性和隔离怎么考虑的？
4. 模型输出是怎么变成真实命令的？（parser 的作用）
5. `submit` 之后 patch 是怎么生成的？（git diff）
6. SWE-bench 是什么？"解决率"怎么计算？
7. litellm 在项目里起什么作用？（统一多模型 API）
8. 上下文窗口有限，长任务怎么办？（history processor 压缩）
9. 和 AutoGPT / MetaGPT / Devin 这类 agent 框架比，Code-Fixer 的特点是什么？
10. 官方为什么转向 mini-swe-agent？两者差在哪？

---

## 附：Java → Python 对照速查表（D1 用，可贴桌边）

| 概念 | Java | Python |
|---|---|---|
| 变量 | `int x = 1;` | `x = 1`（动态类型） |
| 常量 | `final int MAX = 10;` | `MAX = 10`（约定大写） |
| 列表 | `List<Integer> xs = new ArrayList<>();` | `xs = [1, 2, 3]` |
| 字典 | `Map<String, Integer> m = new HashMap<>();` | `m = {"a": 1}` |
| 循环 | `for (int i = 0; i < n; i++)` | `for i in range(n):` |
| 增强 for | `for (String s : list)` | `for s in xs:` |
| 字符串格式化 | `String.format("%s=%d", k, v)` | `f"{k}={v}"` |
| 三元 | `a > b ? a : b` | `a if a > b else b` |
| 流式处理 | `list.stream().map(...).filter(...)` | `[x*2 for x in xs if x > 0]` |
| 类 | `class Foo { private int x; }` | `class Foo: def __init__(self, x): self.x = x` |
| POJO/record | `record Foo(int x) {}` | `@dataclass class Foo: x: int` |
| getter/setter | `getX()` / Lombok | `@property` / 直接属性访问 |
| 注解+AOP | `@Override`, `@Transactional` | `@decorator`（函数包装） |
| try-with-resources | `try (var r = open()) {}` | `with open(...) as f:` |
| 异常 | `try/catch/finally` | `try/except/finally` |
| 泛型 | `List<String>` | 类型注解 `xs: list[str]`（不强制） |
| 接口 | `interface` / `implements` | 鸭子类型（有该方法即可） |
| 测试 | JUnit `@Test` | pytest `def test_x():` |
| 构建 | Maven/Gradle `pom.xml` | `pyproject.toml` + `uv`/`pip` |
| 日志 | slf4j `logger.info()` | `logging.getLogger(__name__)` |
| 配置校验 | Jackson + Bean Validation | **pydantic**（声明即校验+序列化） |

---

## 学习方法提醒

- **先大脑后手脚**：主线 = Agent 循环（想→说→做→看→再想），环境层是支撑它的"手脚"，功能理解即可，细节后补。
- **先主线后细节**：每天先看入口和主流程，再深入局部；别第一天就扣 parser。
- **代码 + 日志对照**：跑一次任务，边看日志边定位代码行，理解最快（你已有 run_*.log 可对照）。
- **善用 `--help_option`**：`codefixer run --help_option codefixer.environment.swe_env.EnvironmentConfig` 能列出某段配置的所有字段（只读，不改配置）。
- **看不懂先放过**：`models.py` 细节、`reviewer.py`、`inspector/`、`action_sampler.py` 不影响主线，有余力再看。
- **Java 思维陷阱提醒**：Python 没有接口强制、没有编译期检查、缩进是语法——阅读时注意 `__init__`/`self`、`dataclass`、`@property`、`with` 这几个和 Java 差异最大的点。
