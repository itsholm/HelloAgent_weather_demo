## 天气助手 ReAct Agent

一个基于 ReAct 模式的简单智能体 Demo：通过 LLM 调用真实工具（天气查询、景点推荐），给出对话式回答。

### 功能简介

- **ReAct 智能体**：根据系统 Prompt 选择调用不同工具，多轮 `Thought` / `Action` / `Observation` 推理。
- **天气查询工具**：调用 `wttr.in` 接口，获取真实城市天气信息。
- **景点推荐工具**：基于 Tavily Search API，根据城市与天气推荐景点。
- **交互式命令行**：支持循环输入查询，持续对话，输入 `exit`/`quit`/`q` 退出
- **完善的日志系统**：支持多级别日志（DEBUG/INFO/WARNING/ERROR），同时输出到控制台和文件，自动日志轮转

### 项目结构
```
helloagent_天气助手/
├── main.py                 # 主程序入口（交互式循环输入）
├── ReActAgent.py           # 智能体核心逻辑（循环调用 LLM、解析 Action、调度工具）
├── callmodel.py            # 对 OpenAI Chat Completions 接口的封装
├── ToolExecutor.py         # 统一管理工具注册与调用
├── get_weather.py          # 天气查询工具（wttr.in API）
├── get_attraction.py       # 景点搜索工具（Tavily Search API）
├── systemprompt.py         # ReAct Prompt 模板
├── logger_config.py        # 日志配置模块
├── requirements.txt        # 项目依赖
├── README.md               # 项目说明文档
├── LOGGING_GUIDE.md        # 日志功能详细使用指南
└── .gitignore              # Git 忽略文件配置
```

### 环境配置

项目依赖以下环境变量（在项目根目录创建 `.env` 文件，配置以下环境变量）：

- `LLM_MODEL_ID`：模型 ID（如 `gpt-4.1-mini` 或其他兼容 OpenAI 协议的模型名称）。
- `LLM_API_KEY`：LLM 服务的 API Key。
- `LLM_BASE_URL`：LLM 服务的 Base URL。
- `TAVILY_API_KEY`：Tavily Search API 的密钥。

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行示例

```bash
python test.py
```

默认示例问题为：“根据南京今天的天气帮我推荐景点？”  
你也可以修改 `test.py` 中的 query，或改造成命令行输入。

### 后续可改进方向

- 更完善的日志与错误处理（如将 `print` 换成 logging）。
- 为 ReAct 步骤增加超时 / 失败重试机制。
- 增加单元测试，覆盖工具函数与解析逻辑。
- 封装为一个可复用的 Python 包或命令行工具。


