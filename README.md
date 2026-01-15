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

### 交互式运行（推荐）

```bash
python main.py
```
程序启动后，会进入交互式循环：
```
============================================================
天气助手 ReAct Agent
输入你的问题，输入 exit / quit / q 可退出
示例：根据南京今天的天气帮我推荐景点？
============================================================

用户输入: 根据南京今天的天气帮我推荐景点？

Step 1:
观察: 南京当前天气:Sunny，气温0摄氏度

Step 2:
观察: [景点推荐结果]

回答: [智能体生成的最终答案]
```

### 退出程序

在交互式界面中输入以下任意命令即可退出：
- `exit`
- `quit`
- `q`

## 日志功能

项目集成了完善的日志系统，支持：

### 日志级别

- **DEBUG**：详细的调试信息（如 LLM 的原始响应）
- **INFO**：一般信息（工具调用、步骤记录）
- **WARNING**：警告信息（达到最大步数、解析失败）
- **ERROR**：错误信息（API 调用失败、异常堆栈）

### 日志输出

- **控制台输出**：实时查看程序运行状态
- **文件输出**：所有日志自动保存到 `helloagent.log` 文件
- **自动轮转**：当日志文件超过 10MB 时，自动创建新文件并保留最近 5 个备份

##  后续改进方向

- [ ] 支持更多天气数据源
- [ ] 增加工具调用的超时和重试机制
- [ ] 添加单元测试
- [ ] 支持流式输出（Streaming）
- [ ] 封装为可复用的 Python 包
- [ ] 添加 Web 界面

**注意**：使用前请确保已正确配置所有必需的环境变量，特别是 LLM API 和 Tavily API 的密钥。



