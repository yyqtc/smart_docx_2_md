# Docx to Markdown 转换工具

一个基于AI的智能Docx文档转Markdown工具，能够自动提取Docx文档中的文本和图片，并生成结构化的Markdown文档。

## ✨ 功能特点

- 🤖 **AI驱动**：使用通义千问大模型进行智能文档结构优化
- 📄 **完整转换**：支持Docx文档(.docx)到Markdown的完整转换
- 🖼️ **图片提取**：自动提取Docx文档中的图片并保存到独立目录
- 🎨 **智能美化**：AI自动优化Markdown文档结构，提升可读性
- 📁 **项目管理**：为每个转换项目创建独立的目录结构
- 🔧 **简单易用**：命令行交互式操作，用户友好

## 🚀 快速开始

### 环境要求

- Python 3.8+
- 通义千问API密钥

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/yyqtc/docx_2_md.git
   cd docx_2_md
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置API密钥**
   
   复制配置文件模板：
   ```bash
   cp config.default.json config.json
   ```
   
   编辑 `config.json` 文件，填入你的API密钥：
   ```json
   {
       "QWEN_API_KEY": "your-qwen-api-key",
       "QWEN_API_BASE": "https://dashscope.aliyuncs.com/compatible-mode/v1",
       "DOCX_DIR_PATH": "./docx",
       "MD_DIR_PATH": "./output"
   }
   ```

4. **准备Docx文档**
   
   将需要转换的Docx文档(.docx格式)放入 `docx/` 目录中。

5. **运行程序**
   ```bash
   python main.py
   ```

## 📖 使用说明

### 基本使用流程

1. **启动程序**：运行 `python main.py`
2. **输入文件名**：程序会提示你输入要转换的Docx文件名
3. **自动处理**：程序会自动完成以下步骤：
   - 检查文件是否存在
   - 创建输出项目目录
   - 提取图片到 `img/` 子目录
   - 转换文档内容为Markdown
   - AI智能美化文档结构
   - 保存最终结果

### 输出结构

转换完成后，会在 `output/` 目录下生成如下结构：

```
output/
└── [项目名称]/
    ├── img/                    # 提取的图片文件
    │   ├── img_1.jpg
    │   ├── img_2.png
    │   └── ...
    └── [项目名称].md           # 转换后的Markdown文档
```

### 示例

假设你有一个名为 `技术文档.docx` 的Docx文件：

1. 将文件放入 `docx/` 目录
2. 运行程序并输入：`技术文档.docx`
3. 程序会在 `output/技术文档/` 目录下生成：
   - `技术文档.md` - 转换后的Markdown文档
   - `img/` - 包含所有提取的图片

## 🔧 配置说明

### config.json 配置项

| 配置项 | 说明 | 示例值 |
|--------|------|--------|
| `QWEN_API_KEY` | 通义千问API密钥 | `sk-xxxxxxxxxx` |
| `QWEN_API_BASE` | API基础URL | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| `DOCX_DIR_PATH` | Docx文档存放目录 | `./docx` |
| `MD_DIR_PATH` | Markdown输出目录 | `./output` |

### 目录结构

```
smart_docx_2_md/
├── main.py              # 主程序入口
├── tool.py              # 核心转换工具
├── custome_type.py      # 自定义数据类型
├── config.json          # 配置文件(将config.default.json的.default去掉)
├── requirements.txt     # 依赖包列表
├── docx/                # Docx文档存放目录
│   ├── 文档1.docx
│   └── 文档2.docx
└── output/              # 输出目录
    ├── 项目1/
    └── 项目2/
```

## 🛠️ 技术架构

- **AI模型**：通义千问 (qwen-plus)
- **框架**：LangChain
- **文档处理**：python-docx
- **类型系统**：Pydantic

## 📝 注意事项

1. **文件格式**：仅支持 `.docx` 格式的Docx文档
2. **API限制**：需要有效的通义千问API密钥
3. **内容保护**：AI美化过程会保持原文档内容完整性，只优化结构
4. **图片处理**：支持的图片格式包括 PNG、JPG、JPEG、GIF、BMP、WEBP

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

本项目采用 MIT 许可证。

---

**提示**：首次使用前请确保已正确配置API密钥，并将Docx文档放置在正确的目录中。
