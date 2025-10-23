from langchain_openai import ChatOpenAI
from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from tool import tools

import asyncio
import json

config = json.load(open("./config.json", encoding="utf-8"))

def _initiate_agent():
    _llm = ChatOpenAI(
        model="qwen-plus",
        openai_api_key=config["QWEN_API_KEY"],
        openai_api_base=config["QWEN_API_BASE"],
        temperature=0.6
    )

    system_prompt = """
        你是一位专业的且话不多的助手，总是能够以最简洁的、最准确的方式回答问题。你能够使用以下能力：
        {tools}

        你能够调用的能力的名称为：{tool_names}

        你可以选择调用能力或是得到最终答案
        当你认为需要调用能力时，必须按照以下JSON格式进行响应：
        {{
            "action": "能力的名称（必须是上述能力之一）",
            "action_input": {{
                "参数名": "参数值"
            }}
        }}

        如果你认为可以得出最终答案了，并按照以下JSON格式进行响应：
        {{
            "action": "Final Answer",
            "action_input": {{
                "output": "你的最终答案"
            }}
        }}

        注意！
        你只能选择调用能力或是得出最终答案。
        如果你发现没有符合你目的的能力，请尝试使用你的现有知识进行回答。
        你的响应必须符合JSON格式规范，不要添加任何多余的字符串。
    """

    human_prompt = """
        {input}

        {agent_scratchpad}

        注意务必按照JSON格式输出！
    """

    _prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", human_prompt)
    ])

    agent = create_structured_chat_agent(
        llm=_llm,
        tools=tools,
        prompt=_prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=100,
        handle_parsing_errors=True
    )

    return agent_executor

def main():
    agent_executor = _initiate_agent()

    while True:
        user_input = input("请输入你希望转换的word文件：")
                    
        prompt = f"""
            你是一位专业的助手，具有结构化思维和审美能力。
            我希望你能够将WORD文档转换为MD文档，并进行美化。
            用户输入的文件名是：{user_input}
            你应该默认认为用户输入的文件名和本系统存储的WORD文件有关。
            首先，你应该判断用户输入的文件存储在本系统且格式正确，如果不存在或格式不正确，直接输出“该文件不存在或格式不正确”作为最终答案。
            如果存在且格式正确，你应该创建一个MD项目目录，并默认后续所有操作都在这个目录下进行，默认MD项目涉及到的资源只有图片资源。如果目录创建失败，你应该尝试创建另一个目录。
            如果目录创建成功，你应该将用户指定的WORD文件转换为MD文件。如果转换失败，直接输出“文件转换失败”作为最终答案。
            如果转换成功，你应该读取转换后的MD文件，并按照结构化思维进行美化。
            你在美化MD文档时，你只可以改变文档的结构，而必须完全保留原文档的内容，不要破坏文档的先后关系，不要修改图片的路径，不要删除原文档的内容！
            最后将美化后的MD文件保存到原MD文档中。

            注意！
            创建一个目录即可，不要反复创建目录！
            你在美化MD文档时，你只可以改变文档的结构，而必须完全保留原文档的内容，不要破坏文档的先后关系，不要修改图片的路径，不要删除原文档的内容！
            你在美化MD文档时，你只可以改变文档的结构，而必须完全保留原文档的内容，不要破坏文档的先后关系，不要修改图片的路径，不要删除原文档的内容！
            你在美化MD文档时，你只可以改变文档的结构，而必须完全保留原文档的内容，不要破坏文档的先后关系，不要修改图片的路径，不要删除原文档的内容！
        """

        asyncio.run(agent_executor.ainvoke({"input": prompt}))

if __name__ == "__main__":
    main()
