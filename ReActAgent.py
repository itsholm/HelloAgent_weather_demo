from systemprompt import REACT_PROMPT_TEMPLATE
from ToolExecutor import ToolExecutor
from callmodel import HelloAgentLLM
import re
import json
import logging

# 获取当前模块的 logger（使用模块名作为 logger 名称）
logger = logging.getLogger(__name__)

class ReActAgent:
    def __init__(self,llm_client:HelloAgentLLM,tool_executor:ToolExecutor,max_steps:int=3):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.max_steps = max_steps
        self.history = []

    def run(self,query:str):
        self.history = []
        current_step = 0
        #1,格式化系统提示词
        tools_desc= self.tool_executor.listTools()
        system_prompt=REACT_PROMPT_TEMPLATE.format(tools=tools_desc)
        #print(system_prompt)

        while current_step<self.max_steps:
            current_step += 1
            print(f"Step {current_step}:")
            logger.info(f"Step {current_step}:")
            #构建uesr_message,包含原始query和历史
            if self.history:
            # self.history 是字符串列表，如 ["Action: ...", "Observation: ..."]
                history_str = "\n".join([f"{i+1}. {msg}" for i, msg in enumerate(self.history)])
                user_message = f"Query:{query}\nHistory:\n{history_str}"
            else:
                user_message = f"Query:{query}"

            #2,调用LLM生成响应
            messages = [ #把prompt包装成messages格式
                {"role":"system","content":system_prompt},
                {"role":"user","content":user_message}
            ]

            response = self.llm_client.generate_response(messages)
            if response is None:
                print("警告: LLM 返回为空，流程终止。")
                logger.warning("LLM 返回为空，流程终止。")
                break
            # 记录 LLM 的原始输出（DEBUG 级别，生产环境可以关闭）
            # print(">>> LLM 输出 (raw response):\n",response)
            logger.debug(f"LLM 原始输出:\n{response}")
            logger.info(f"LLM 响应已接收（长度: {len(response)} 字符）")

            thought,action = self._parse_response(response)

            #if thought:
                #print(f"思考：{thought}")
            
            if not action:
                #print("警告:未能解析出有效的Action，流程终止。")
                logger.warning("未能解析出有效的Action，流程终止。")
                break

            #-----------4.执行action-----------------
            #4.1走Finish指令
            if action.startswith("Finish"):
                #如果是Finish指令提取最终答案
                final_answer = re.match(r"Finish\((.*)\)",action).group(1)
                #print(f"最终答案：{final_answer}")
                logger.info(f"完成推理，最终答案: {final_answer}")
                return final_answer
            
            #4.2走Tool指令
            #解析工具
            tool_name,tool_input = self._parse_action(action)
            if not tool_name or not tool_input:
                #print("Action解析错误")
                logger.error(f"Action解析错误: {action}")
                continue#无效action格式
            
            tool_func = self.tool_executor.getTool(tool_name)
            if not tool_func:
                observation = f"错误:未找到名为'{tool_name}'的工具。"
                logger.error(observation)
            else:
                logger.info(f"调用工具: {tool_name}, 参数: {tool_input}")
                try:
                    if isinstance(tool_input, dict):
                        observation = tool_func(**tool_input)
                    else:
                        observation = tool_func(tool_input)
                    logger.info(f"工具执行成功，返回结果长度: {len(str(observation))} 字符")
                except Exception as e:
                    observation = f"错误:工具执行失败 - {e}"
                    logger.error(f"工具 {tool_name} 执行异常: {e}", exc_info=True)
            
            print(f"👀观察: {observation}")
            logger.debug(f"观察结果: {observation}")
            # !!!!!将本轮的Action和Observation添加到历史记录中 !!!!!
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")

        # 达到最大步数时，尝试从历史中提取答案
        logger.warning(f"已达到最大步数 ({self.max_steps})，尝试从历史中提取答案...")
        
        # 如果历史中有观察结果，尝试让 LLM 生成最终答案
        if self.history:
            # 构建一个提示，要求 LLM 基于已有信息给出最终答案
            final_prompt = f"""基于以下查询和历史信息，请给出最终答案：

查询: {query}

历史信息:
{chr(10).join(self.history)}

请直接给出简洁的最终答案，不需要再调用工具。"""
            
            messages = [
                {"role": "system", "content": "你是一个助手，请根据提供的信息给出最终答案。"},
                {"role": "user", "content": final_prompt}
            ]
            
            final_response = self.llm_client.generate_response(messages, max_tokens=512)
            if final_response:
                # 清理响应（移除可能的 Thought/Action 标记）
                final_answer = final_response.strip()
                # 如果响应中包含 "Thought:" 或 "Action:"，尝试提取实际答案部分
                if "Thought:" in final_answer:
                    parts = final_answer.split("Thought:")
                    if len(parts) > 1:
                        final_answer = parts[-1].strip()
                if "Action:" in final_answer:
                    parts = final_answer.split("Action:")
                    final_answer = parts[0].strip()
                
                print(f"最终答案（从历史提取）: {final_answer}")
                logger.info(f"从历史中提取到最终答案: {final_answer[:100]}...")
                return final_answer
        
        logger.warning("无法从历史中提取有效答案")
        return None #返回类型为None，不能使用迭代器

    def _parse_response(self,response:str)->str:
        """
        解析LLM的响应，提取Action和Tool调用信息
        """
        thought_match = re.search(r"Thought: (.*)", response, re.DOTALL)
        action_match = re.search(r"Action: (.*)", response, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thought, action

    #JSON格式在多参数下更健壮
    def _parse_action(self, action_str: str):
        # 匹配格式：函数名(JSON参数串)
        # 例如：get_weather({"city": "南京", "unit": "C"})
        match = re.match(r"(\w+)\((.*)\)", action_str, re.DOTALL)
        if match:
            tool_name = match.group(1)
            params_str = match.group(2).strip()

            try:
                # 尝试将括号内的内容解析为 JSON 对象（字典）
                # 这种方式天然支持多参数和复杂类型
                params = json.loads(params_str)
                return tool_name, params
            except json.JSONDecodeError:
                # 如果不是 JSON，尝试当作普通字符串处理（向前兼容）
                return tool_name, params_str.strip('"\'')
            
        return None, None

 #去掉参数的双引号，但只对单个参数有用   
    # def _parse_action(self, action_text: str):
    #     """解析Action字符串，提取工具名称和输入。"""
    #     match = re.match(r"(\w+)\((.*)\)", action_text)
    #     if match:
    #         tool_name = match.group(1)
    #         tool_input = match.group(2).strip()
    #     if (tool_input.startswith("'") and tool_input.endswith("'")) or \
    #        (tool_input.startswith('"') and tool_input.endswith('"')):
    #         tool_input = tool_input[1:-1]
    #         return tool_name, tool_input
    #     return None, None