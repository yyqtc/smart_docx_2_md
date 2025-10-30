from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from tool import mkdir_md_project, revert_and_save_md_file, read_md_file, save_md_file

import json
import time
import os

config = json.load(open("./config.json", encoding="utf-8"))

def main():
    system_prompt_1 = ChatPromptTemplate.from_messages([
        ("system", """
            你是一位专业的助手。
            请你帮我根据用户输入的docx文件名，生成一个markdown文件夹的名字。
            只返回文件夹名字，不要返回任何多余的内容。
            注意！
            1. 文件夹名不能包含特殊字符，只能包含字母、汉字、数字和下划线。
            2. 如果用户提示项目名已被占用，你生成的项目名必须和被占用项目名不同。
        """),
        ("placeholder", "{messages}")
    ])

    _llm = ChatOpenAI(
        model="qwen-plus",
        openai_api_key=config["QWEN_API_KEY"],
        openai_api_base=config["QWEN_API_BASE"],
        temperature=0.4
    )

    md_name_assistant = system_prompt_1 | _llm

    system_prompt_2 = ChatPromptTemplate.from_messages([
        ("system", """
            你是一位专业的助手。
            请你帮我根据用户输入的markdown内容，美化markdown文档的结构。
            美化规则是：
                1. 你不允许修改内容，只能美化文档的结构。
                2. 你必须按照markdown的语法进行美化。
                3. 你不能改变段落的前后顺序。
            
            注意！
            1. 你返回的文档内容必须符合markdown格式，但内容不要带上```markdown。
            2. 你只返回美化后的markdown文档内容，不要返回任何多余的内容。
        """),
        ("placeholder", "{messages}")
    ])

    md_pretty_assistant = system_prompt_2 | _llm
    
    while True:
        user_input = input("请输入你希望转换的docx文件：")

        if user_input == "exit":
            break

        doc_name = user_input            
        if not user_input.endswith(".docx"):
            doc_name = doc_name + ".docx"

        if not os.path.exists(os.path.join(config["DOCX_DIR_PATH"], doc_name)):
            print(f"文件{doc_name}不存在，请重新输入。")
            continue

        user_input = f"请根据doc文件名{doc_name}，美化markdown文档的结构。"

        markdown_project_name = ""
        while not markdown_project_name:
            temp_name = md_name_assistant.invoke(
                {"messages": [{"role": "user", "content": user_input}]}
            ).content

            print(f"生成的项目名：{temp_name}")

            if temp_name.endswith(".md"):
                temp_name = temp_name.replace(".md", "")

            if os.path.exists(os.path.join(config["MD_DIR_PATH"], temp_name)):
                user_input += f"\n项目{temp_name}已存在。"
                time.sleep(2)
            else:
                markdown_project_name = temp_name

        markdown_file_name = markdown_project_name + ".md"
        project_structure = mkdir_md_project(markdown_project_name)

        if isinstance(project_structure, str):
            print(f"创建项目{markdown_project_name}失败。")
            continue

        print(f"创建项目{markdown_project_name}成功。")

        revert_result = revert_and_save_md_file(
            doc_name, 
            markdown_project_name, 
            markdown_file_name
        )

        if revert_result != "转换保存成功":
            print(f"文件{doc_name}转换保存失败。")
            continue

        print(f"文件{doc_name}转换保存成功。")

        md_content = read_md_file(markdown_project_name, markdown_file_name)
        if md_content == "文件不存在":
            print(f"文件{markdown_file_name}不存在。")
            continue
        elif md_content == "文件不是MD文件":
            print(f"文件{markdown_file_name}不是MD文件。")
            continue

        print("即将美化markdown结构，这将会是很赞的！")

        prompt = f"请根据markdown文档内容{md_content}，美化markdown文档的结构。"
        md_pretty_content = md_pretty_assistant.invoke(
            {"messages": [{"role": "user", "content": prompt}]}
        ).content

        if md_pretty_content.startswith("```markdown"):
            md_pretty_content = md_pretty_content.replace("```markdown", "")

        print("美化完成！")

        save_result = save_md_file(
            markdown_project_name, 
            markdown_file_name, 
            md_pretty_content
        )

        if save_result != "保存成功":
            print("文件保存失败。")
            continue

        print("文件保存成功。")


if __name__ == "__main__":
    main()
