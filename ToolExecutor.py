#-------工具执行器-------#
#统一管理注册和调度工具的执行
from typing import Dict,Any
import inspect
import logging

logger = logging.getLogger(__name__)

class ToolExecutor:
    def __init__(self):
        self.tools:Dict[str,Dict[str,Any]] = {}
    
    def register_tool(self,name:str,description:str,func):
        """
        向工具箱中注册一个新工具。
        """
        if name in self.tools:
            print(f"工具{name}已存在，将被覆盖")
            logger.warning(f"工具 {name} 已存在，将被覆盖")
        self.tools[name] = {"description":description,"func":func}
        print(f"工具{name}已注册成功")
        logger.info(f"工具 {name} 已注册成功: {description}")

    def getTool(self,name:str)->callable:
        """
        根据名称获取已注册的工具函数。
        """
        return self.tools.get(name,{}).get("func")

    def listTools(self)->str:
        """
        获取所有可用工具的格式化描述字符串
        """
        tool_list = []
        for name,info in self.tools.items():
            func = info['func']
            sig = inspect.signature(func)
            tool_list.append(f"- {name}{sig}: {info['description']}")
        return "\n".join(tool_list)

# # --- 测试代码 ---
# if __name__ == "__main__":
#     executor = ToolExecutor()
    
#     def add(a: int, b: int = 10):
#         return a + b
    
#     def get_weather(city: str, unit: str = "celsius"):
#         return f"Fetching weather for {city}..."

#     executor.register_tool("add_numbers", "计算两个数字之和", add)
#     executor.register_tool("get_weather", "查询天气", get_weather)

#     print("\n当前可用工具列表：")
#     print(executor.listTools())
