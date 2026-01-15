# Logging 功能使用指南

## 📚 什么是 Logging？

`logging` 是 Python 标准库提供的日志记录模块，相比直接使用 `print()`，它有以下几个优势：

1. **日志级别**：可以区分不同重要程度的信息（DEBUG、INFO、WARNING、ERROR）
2. **灵活输出**：可以同时输出到控制台和文件
3. **生产友好**：可以控制日志详细程度，生产环境关闭 DEBUG，开发时开启
4. **便于调试**：记录时间戳、模块名、异常堆栈等信息

---

## 🏗️ 项目中的 Logging 架构

### 1. 日志配置模块 (`logger_config.py`)

这是整个项目的日志配置中心，提供了 `setup_logger()` 函数：

```python
setup_logger(
    name="helloagent",           # logger 名称
    log_level="INFO",            # 日志级别
    log_to_file=True,            # 是否写入文件
    log_file="helloagent.log",   # 日志文件路径
    max_bytes=10*1024*1024,      # 单个文件最大 10MB
    backup_count=5               # 保留 5 个备份文件
)
```

**关键特性：**
- **日志轮转（Rotating）**：当日志文件超过 10MB 时，自动创建新文件，保留最近 5 个备份
- **双重输出**：同时输出到控制台（方便开发）和文件（方便生产环境查看历史）
- **UTF-8 编码**：支持中文日志

### 2. 各模块中的 Logger

每个模块都有自己的 logger，使用模块名（`__name__`）作为标识：

```python
import logging
logger = logging.getLogger(__name__)  # 例如：ReActAgent、callmodel
```

这样做的好处：
- 可以单独控制某个模块的日志级别
- 日志中会显示是哪个模块输出的信息

---

## 📊 日志级别说明

Python logging 有 5 个级别，从低到高：

| 级别 | 数值 | 使用场景 | 示例 |
|------|------|----------|------|
| **DEBUG** | 10 | 详细的调试信息 | LLM 的原始响应内容 |
| **INFO** | 20 | 一般信息，程序正常运行 | "工具已注册"、"Step 1" |
| **WARNING** | 30 | 警告信息，可能有问题但不影响运行 | "已达到最大步数" |
| **ERROR** | 40 | 错误信息，功能可能失败 | "LLM 调用失败" |
| **CRITICAL** | 50 | 严重错误，程序可能无法继续 | 很少使用 |

**重要规则：** 如果设置日志级别为 `INFO`，那么 `DEBUG` 级别的日志不会显示，但 `INFO`、`WARNING`、`ERROR` 都会显示。

---

## 🔧 如何使用

### 基本用法

在代码中使用 logger：

```python
logger.debug("这是调试信息")      # 开发时查看详细过程
logger.info("这是一般信息")       # 正常流程记录
logger.warning("这是警告")        # 需要注意但不影响运行
logger.error("这是错误")          # 错误信息
```

### 记录异常

使用 `exc_info=True` 可以记录完整的异常堆栈：

```python
try:
    result = some_function()
except Exception as e:
    logger.error(f"执行失败: {e}", exc_info=True)
    # 这会记录完整的异常堆栈，方便调试
```

### 格式化输出

logger 支持格式化字符串：

```python
logger.info(f"收到用户查询: {user_query}")
logger.info("调用工具: %s, 参数: %s", tool_name, tool_input)  # 旧式格式化也可以
```

---

## 🎛️ 如何控制日志级别

### 方法 1：修改 `main.py` 中的配置

```python
# 开发时：显示所有信息（包括 DEBUG）
setup_logger("helloagent", log_level="DEBUG", log_to_file=True)

# 生产环境：只显示 INFO 及以上
setup_logger("helloagent", log_level="INFO", log_to_file=True)
```

### 方法 2：使用环境变量

在 `.env` 文件中设置：

```env
LOG_LEVEL=DEBUG
```

然后在 `logger_config.py` 中会自动读取：

```python
default_log_level = os.getenv("LOG_LEVEL", "INFO")
```

### 方法 3：命令行运行时设置

```bash
# Windows
set LOG_LEVEL=DEBUG && python main.py

# Linux/Mac
LOG_LEVEL=DEBUG python main.py
```

---

## 📁 日志文件位置

默认日志文件：`helloagent.log`（项目根目录）

日志轮转示例：
- `helloagent.log`（当前日志）
- `helloagent.log.1`（第一个备份）
- `helloagent.log.2`（第二个备份）
- ...最多保留 5 个

---

## 🔍 实际使用示例

### 示例 1：查看完整的执行流程（DEBUG 模式）

```python
# main.py 中设置
setup_logger("helloagent", log_level="DEBUG", log_to_file=True)
```

运行后会看到：
```
2024-01-15 10:30:45 - helloagent - INFO - 正在初始化智能体组件...
2024-01-15 10:30:45 - ToolExecutor - INFO - 工具 get_weather 已注册成功
2024-01-15 10:30:45 - ReActAgent - INFO - Step 1:
2024-01-15 10:30:45 - callmodel - DEBUG - 调用LLM模型: gpt-4, max_tokens=1024
2024-01-15 10:30:46 - callmodel - INFO - LLM模型调用成功
2024-01-15 10:30:46 - ReActAgent - DEBUG - LLM 原始输出: ...
2024-01-15 10:30:46 - ReActAgent - INFO - 调用工具: get_weather, 参数: {'city': '南京'}
```

### 示例 2：生产环境（INFO 模式）

```python
setup_logger("helloagent", log_level="INFO", log_to_file=True)
```

只会看到关键信息，DEBUG 级别的详细内容不会显示。

---

## 💡 最佳实践

1. **开发阶段**：使用 `DEBUG` 级别，查看所有细节
2. **生产环境**：使用 `INFO` 或 `WARNING` 级别，减少日志量
3. **用户交互**：保留 `print()` 用于直接给用户看的提示（如"请输入问题"）
4. **程序内部**：使用 `logger` 记录所有执行过程、错误信息
5. **异常处理**：使用 `logger.error(..., exc_info=True)` 记录完整堆栈

---

## 🆚 print() vs logger 对比

| 特性 | print() | logger |
|------|---------|--------|
| 输出位置 | 只能控制台 | 控制台 + 文件 |
| 日志级别 | 无 | 5 个级别 |
| 时间戳 | 无 | 自动添加 |
| 模块标识 | 无 | 自动添加模块名 |
| 异常堆栈 | 需要手动 traceback | `exc_info=True` |
| 生产环境 | 难以控制 | 可关闭 DEBUG |
| 日志轮转 | 不支持 | 自动轮转 |

---

## 📝 项目中各模块的日志使用

### `ReActAgent.py`
- `logger.info()`: 记录每个推理步骤、工具调用
- `logger.debug()`: 记录 LLM 的原始输出（开发时查看）
- `logger.warning()`: 达到最大步数、解析失败等警告
- `logger.error()`: Action 解析错误

### `callmodel.py`
- `logger.info()`: LLM 调用成功
- `logger.debug()`: 调用参数详情
- `logger.error()`: 调用失败 + 异常堆栈

### `ToolExecutor.py`
- `logger.info()`: 工具注册成功
- `logger.warning()`: 工具被覆盖

### `main.py`
- `logger.info()`: 用户查询、初始化完成
- `logger.warning()`: 未能生成答案
- `logger.error()`: 处理异常

---

## 🎯 总结

现在你的项目已经具备了完整的日志系统：

✅ **统一配置**：`logger_config.py` 集中管理  
✅ **模块化**：每个模块有自己的 logger  
✅ **灵活控制**：可通过环境变量或代码调整级别  
✅ **双重输出**：控制台 + 文件  
✅ **自动轮转**：避免日志文件过大  
✅ **异常记录**：完整的错误堆栈信息  

运行 `python main.py` 试试，你会看到格式化的日志输出，同时所有日志也会保存到 `helloagent.log` 文件中！

