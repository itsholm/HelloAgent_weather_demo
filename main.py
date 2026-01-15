import logging
from logger_config import setup_logger

from ReActAgent import ReActAgent
from callmodel import HelloAgentLLM
from ToolExecutor import ToolExecutor

from systemprompt import REACT_PROMPT_TEMPLATE
from get_weather import get_weather
from get_attraction import get_attraction  # 你的项目已有该工具

# 初始化日志系统（在程序启动时配置一次即可）
# 可以通过环境变量 LOG_LEVEL 控制日志级别（DEBUG, INFO, WARNING, ERROR）
import os
log_level = os.getenv("LOG_LEVEL", "INFO")
setup_logger(log_level=log_level, log_to_file=True)
logger = logging.getLogger(__name__)

#初始化组件
logger.info("正在初始化智能体组件...")
llm_client = HelloAgentLLM()
executor = ToolExecutor()

#注册工具
executor.register_tool("get_weather", "查询指定城市的实时天气信息，返回格式：城市名当前天气:天气状况，气温X摄氏度", get_weather)
executor.register_tool("get_attraction", "根据城市和完整天气信息（包括天气状况和温度）推荐景点。weather参数应包含完整的天气描述，例如：'Sunny，气温0摄氏度'或'多云，气温20摄氏度'", get_attraction)

# 实例化智能体
agent = ReActAgent(llm_client, executor)
logger.info("智能体初始化完成，准备接收用户查询")

if __name__ == "__main__":
    print("=" * 60)
    print("天气助手 ReAct Agent")
    print("输入你的问题，输入 exit / quit / q 可退出")
    print("示例：根据南京今天的天气帮我推荐景点？")
    print("=" * 60)
    
    while True:
        user_query = input("\n用户输入: ").strip()
        if user_query.lower() in {"exit", "quit", "q"}:
            logger.info("用户退出程序")
            print("已退出。")
            break
        if not user_query:
            print("请输入有效的问题。")
            continue
        
        # 记录用户查询
        logger.info(f"收到用户查询: {user_query}")
        
        try:
            result = agent.run(user_query)
            if result is not None:
                print(f"\n回答: {result}")
                logger.info("成功返回答案给用户")
            else:
                print("\n抱歉，未能生成有效回答。")
                logger.warning("智能体未能生成有效回答")
        except Exception as e:
            logger.error(f"处理用户查询时发生异常: {e}", exc_info=True)
            print(f"\n发生错误: {e}")
