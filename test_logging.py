"""测试日志功能"""
from logger_config import setup_logger
import logging

# 初始化日志系统
setup_logger(log_level="INFO", log_to_file=True)

# 测试各个模块的 logger
logger_main = logging.getLogger(__name__)
logger_react = logging.getLogger("ReActAgent")
logger_callmodel = logging.getLogger("callmodel")
logger_tool = logging.getLogger("ToolExecutor")

print("=" * 60)
print("开始测试日志功能...")
print("=" * 60)

logger_main.info("这是 main 模块的日志")
logger_react.info("这是 ReActAgent 模块的日志")
logger_callmodel.info("这是 callmodel 模块的日志")
logger_tool.info("这是 ToolExecutor 模块的日志")

logger_main.warning("这是一条警告信息")
logger_main.error("这是一条错误信息（测试）")

print("=" * 60)
print("日志测试完成！请检查：")
print("1. 控制台是否有日志输出")
print("2. helloagent.log 文件是否有内容")
print("=" * 60)

