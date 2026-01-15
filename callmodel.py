#=------------封装LLM调用函数------------=#
import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
#import traceback
load_dotenv()

logger = logging.getLogger(__name__)

class HelloAgentLLM:
    def __init__(self,model:str=None,apiKey:str=None,baseUrl:str=None):
        self.model = model or os.getenv("LLM_MODEL_ID")
        apiKey = apiKey or os.getenv("LLM_API_KEY")
        baseUrl = baseUrl or os.getenv("LLM_BASE_URL")

        if not self.model or not apiKey or not baseUrl:
            logger.error("模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")
            raise ValueError("模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")

        self.client = OpenAI(api_key=apiKey,base_url=baseUrl)

    def generate_response(self,messages:list[dict[str,str]],max_tokens:int=1024,temperature:float=0.7):
        logger.debug(f"调用LLM模型: {self.model}, max_tokens={max_tokens}, temperature={temperature}")
        try:
            response = self.client.chat.completions.create(
                model = self.model,
                messages = messages,
                max_tokens = max_tokens,
                temperature = temperature,
                extra_body={"enable_thinking": False}  #关键修复！
                #OpenAI SDK 提供的扩展机制
            )
            print("调用LLM模型成功")
            logger.info("LLM模型调用成功")
            return response.choices[0].message.content.strip()  # 去除首尾空格
        except Exception as e:
            print(f"调用LLM模型失败: {e}")
            #traceback.print_exc()  # 打印完整错误堆栈，这能告诉我到底是什么问题
            logger.error(f"调用LLM模型失败: {e}", exc_info=True)
            # exc_info=True 会记录完整的异常堆栈信息
            return None

# #----测试----#
# if __name__ == "__main__":
#     llm = HelloAgentLLM() #实例化类
#     messages = [
#         {"role":"system","content":"你是一个助手，回答用户的问题。"},
#         {"role":"user","content":"你好，你是谁？"}
#     ]
#     response = llm.generate_response(messages)
#     print(response)
