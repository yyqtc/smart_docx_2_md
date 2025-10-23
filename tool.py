from langchain.tools import tool
from custome_type import ProjectStruct
from typing import Union, List
from docx import Document

import os
import json

config = json.load(open("./config.json", encoding="utf-8"))

def _revert_word_to_md(doc: Document, md_project_name: str) -> str:
    image_map = {}
    image_count = 0

    for rel in doc.part.rels.values():
        if 'image' in rel.reltype:
            image_count += 1
            image_data = rel.target_part.blob
            ext = rel.target_part.partname.split("/")[-1].split(".")[-1].lower()
            if ext not in ["png", "jpg", "jpeg", "gif", "bmp", "webp"]:
                ext = "jpg"
            
            image_name = f"img_{image_count}.{ext}"
            image_path = os.path.join(config["MD_DIR_PATH"], md_project_name, "img", image_name)
            with open(image_path, "wb") as f:
                f.write(image_data)
            image_map[rel.rId] = f'./img/{image_name}'

    image_count = 0
    full_text = ""

    for para in doc.paragraphs:
        for run in para.runs:
            for child in run._element.getchildren():
                if child.tag.endswith("}drawing") or child.tag.endswith("}pict"):
                    blips = child.xpath(".//*[local-name()='blip']")
                    
                    if blips:
                        rId = blips[0].get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                        if rId:
                            if rId in [r.rId for r in doc.part.rels.values()]:
                                image_count += 1
                                image_path = image_map.get(rId, f"img_{image_count}.jpg")
                                print(image_path, rId)
                                full_text += f"\n\n![图片{image_count}]({image_path})\n\n"

                elif child.tag.endswith("}t"):
                    text = child.text or ""
                    full_text += text
        full_text += "\n"

    return full_text.strip()
        
@tool
def get_word_list() -> List[str]:
    """
    获取本系统存放的PDF文件名列表。

    Args:
        无

    Returns:
        返回本系统存放的PDF文件名列表。
    """

    filelist = os.listdir(config["WORD_DIR_PATH"])
    return [file for file in filelist if file.endswith(".docx")]

@tool
def revert_and_save_md_file(word_name: str, md_project_name: str, md_file_name: str) -> str:
    """
    将WORD文件转换为MD文件，并保存到指定MD项目目录中。
    转换后务必对该MD文件按照结构化思维进行美化。
    
    Args:
        word_name: WORD文件名称
        md_project_name: MD项目名称
        md_file_name: MD文件名称，必须以.md结尾
    
    Returns:
        如果word文件不存在，则返回"word文件不存在"
        如果文件不是word文件，则返回"文件不是word文件"
        如果md文件路径已经存在，则返回"md文件已存在"
        如果word文件存在，则将WORD文件转换为MD文件并保存在指定MD项目目录中，如果转换保存成功，则返回"转换保存成功"，否则返回"转换保存失败"
    """

    word_path = os.path.join(config["WORD_DIR_PATH"], word_name)
    md_path = os.path.join(config["MD_DIR_PATH"], md_project_name, md_file_name)

    if not os.path.exists(word_path) or not os.path.isfile(word_path):
        return "word文件不存在"
    elif not word_path.endswith(".docx"):
        return "文件不是word文件"
    elif os.path.exists(md_path):
        return "md文件已存在"
    else:
        doc = Document(word_path)
        try:
            md_file_content = _revert_word_to_md(doc, md_project_name)

            with open(md_path, 'w+', encoding="utf-8") as f:
                f.write(md_file_content)

            return "转换保存成功"
        except Exception as e:
            print("转换过程中出错：", e)
            return "转换保存失败"

@tool
def mkdir_md_project(md_project_name: str) -> Union[ProjectStruct, str]:
    """
    创建一个md5项目目录，并返回项目

    Args:
        md_project_name: md项目名称

    Returns:
        如果md_project_name已经存在，则返回"项目已存在"
        如果md_project_name不存在，则创建一个md项目目录，并返回项目信息，包括MD项目名称、MD项目图片目录路径
    """
    
    project_path = os.path.join(config["MD_DIR_PATH"], md_project_name)

    if not os.path.exists(project_path):
        os.makedirs(project_path)
        image_dir_path = os.path.join(project_path, "img")
        os.makedirs(image_dir_path)

        return {
            "project_name": md_project_name,
            "image_dir_path": f"{md_project_name}/img"
        }
    else:
        return "项目已存在"

@tool
def count_md_file_len(md_project_name: str, md_file_name: str) -> int:
    """
    获取MD文件内容总字符数

    Args:
        md_project_name: MD项目名称
        md_file_name: MD文件名称，必须以.md结尾

    Returns:
        如果指定文件不存在，则返回0。
        如果指定文件不是MD文件，则返回0。
        如果指定文件存在且是MD文件，则返回该文件内容总字符数。
    """
    
    md_file_path = os.path.join(config["MD_DIR_PATH"], md_project_name, md_file_name)
    
    if not os.path.exists(md_file_path) or not os.path.isfile(md_file_path):
        return 0
    elif not md_file_path.endswith(".md"):
        return 0
    else:
        with open(md_file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return len(content)

@tool
def read_md_file_with_limit(md_project_name: str, md_file_name: str, prefix: int, limit: int) -> str:
    """
    读取MD文件内容，并返回指定长度的内容。

    Args:
        md_project_name: MD项目名称
        md_file_name: MD文件名称，必须以.md结尾
        prefix: 内容起始偏移量，最小值为0
        limit: 最大字符数限制，最小值为1

    Returns:
        如果指定文件不存在，则返回"文件不存在"
        如果指定文件不是MD文件，则返回"文件不是MD文件"
        如果指定文件存在且是MD文件，则返回指定范围的内容
    """

    md_file_path = os.path.join(config["MD_DIR_PATH"], md_project_name, md_file_name)

    if not os.path.exists(md_file_path) or not os.path.isfile(md_file_path):
        return "文件不存在"
    elif not md_file_path.endswith(".md"):
        return "文件不是MD文件"
    else:
        with open(md_file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content[prefix:prefix+limit]

@tool
def save_md_file(md_project_name: str, md_file_name: str, md_file_content: str) -> str:
    """
    将MD文件内容保存到指定MD文件中。
    注意这个函数会对MD文件造成不可逆的修改，请谨慎使用。

    Args:
        md_project_name: MD项目名称
        md_file_name: MD文件名称，必须以.md结尾
        md_file_content: MD文件内容

    Returns:
        如果指定文件不存在，则返回"文件不存在"
        如果指定文件不是MD文件，则返回"文件不是MD文件"
        如果指定文件存在且是MD文件，则将MD文件内容保存到指定MD文件中，如果保存成功，则返回"保存成功"，否则返回"保存失败"
    """

    md_file_path = os.path.join(config["MD_DIR_PATH"], md_project_name, md_file_name)

    if not os.path.exists(md_file_path) or not os.path.isfile(md_file_path):
        return "文件不存在"
    elif not md_file_path.endswith(".md"):
        return "文件不是MD文件"
    else:
        with open(md_file_path, "w+", encoding="utf-8") as f:
            f.write(md_file_content)
        return "保存成功"

tools = [
    get_word_list,
    revert_and_save_md_file,
    mkdir_md_project,
    count_md_file_len,
    read_md_file_with_limit,
    save_md_file
]
