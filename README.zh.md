<div align="center">
  <p>
    <a href="README.zh.md">中文</a> | 
    <a href="README.md">English</a>
  </p>
  
  <h1>🐣inquirer_console</h1>
  <p>优雅的交互式命令行界面工具库</p>
  
  <p>
    <a href="#-安装"><strong>安装指南</strong></a> •
    <a href="#-特性"><strong>特性</strong></a> •
    <a href="#-使用示例"><strong>使用示例</strong></a> •
    <a href="#-api文档"><strong>API文档</strong></a> •
    <a href="#-贡献指南"><strong>贡献指南</strong></a>
  </p>
  
  <p>
    <img alt="Python Version" src="https://img.shields.io/badge/Python-3.12%2B-blue?style=flat-square&logo=python">
    <img alt="License" src="https://img.shields.io/badge/License-MIT-green?style=flat-square">
    <img alt="PRs Welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square">
  </p>
</div>

## 📖 简介

inquirer_console 是 [Inquirer.js](https://github.com/SBoudrias/Inquirer.js) 的 Python 实现，提供了一组精心设计的交互式命令行用户界面组件，让开发者能够轻松创建美观、人性化的命令行应用程序。

## ✨ 特性

- **跨平台兼容** - 完美支持 Windows、macOS 和各种 Linux/Unix 系统
- **优雅的中断处理** - 智能处理 Ctrl+C，确保用户体验流畅
- **强大的输入验证** - 通过自定义 validate 函数轻松验证用户输入
- **灵活的数据转换** - 通过 filter 函数实时转换用户输入
- **链式 API** - 提供类似 Inquirer.js 的流畅 API，简化复杂交互
- **完全类型注解** - 全面的类型提示，提升开发体验
- **零外部依赖** - 纯 Python 标准库实现，无需额外安装

## 🧩 提示类型

inquirer_console 目前实现了以下提示类型：

| 类型 | 描述 | 预览 |
|------|------|------|
| **Input** | 文本输入提示 | `> 请输入您的名字：` |
| **Confirm** | 确认提示（是/否） | `> 是否继续？ (Y/n)：` |
| **Select** | 列表选择提示（单选） | `> 选择一个选项：❯ 选项1 ⬡ 选项2 ⬡ 选项3` |
| **Checkbox** | 复选框提示（多选） | `> 选择多个选项：❯ [X] 选项1 [ ] 选项2 [X] 选项3` |
| **Password** | 密码输入提示 | `> 请输入密码：******` |
| **Text** | 多行文本输入提示 | `> 请输入描述：(连续两次按Enter结束输入)` |

## 🚀 安装

目前处于开发阶段，您可以通过以下方式安装：

```bash
# 从 PyPI 安装
pip install inquirer_console

# 直接从 GitHub 安装
pip install git+https://github.com/Eusen/inquirer_console.git

# 或者克隆仓库使用
git clone https://github.com/Eusen/inquirer_console.git
cd inquirer_console
pip install -e .
```

## 📝 使用示例

### 单独使用各个提示类型

```python
from inquirer_console import Input, Confirm, Select, Checkbox, Password, Text

# 输入提示
name = Input(
    message="你的名字是",
    validate=lambda val: True if val else "名字不能为空！"
).prompt()

# 确认提示
likes_python = Confirm(
    message="你喜欢Python吗",
    default=True
).prompt()

# 选择提示
favorite_lang = Select(
    message="你最喜欢的编程语言是",
    choices=[
        {'name': 'Python', 'value': 'python'},
        {'name': 'JavaScript', 'value': 'js'},
        {'name': 'Rust', 'value': 'rust'}
    ]
).prompt()

# 复选框提示
languages = Checkbox(
    message="你会使用哪些编程语言",
    choices=[
        {'name': 'Python', 'value': 'python', 'checked': True},
        {'name': 'JavaScript', 'value': 'js'},
        {'name': 'Rust', 'value': 'rust'}
    ]
).prompt()

# 密码提示
password = Password(
    message="请输入一个密码",
    validate=lambda val: True if len(val) >= 6 else "密码至少需要6个字符！"
).prompt()

# 多行文本提示 (连续两次按Enter结束输入)
description = Text(
    message="请输入项目描述"
).prompt()
```

### 使用 inquirer 链式调用

```python
from inquirer_console import inquirer

# 定义问题列表
questions = [
    {
        'type': 'input',
        'name': 'name',
        'message': '你的名字是',
        'validate': lambda val: True if val else "名字不能为空！"
    },
    {
        'type': 'confirm',
        'name': 'likes_python',
        'message': '你喜欢Python吗',
        'default': True
    },
    {
        'type': 'list',
        'name': 'favorite_lang',
        'message': '你最喜欢的编程语言是',
        'choices': [
            {'name': 'Python', 'value': 'python'},
            {'name': 'JavaScript', 'value': 'js'},
            {'name': 'Rust', 'value': 'rust'}
        ]
    },
    {
        'type': 'text',
        'name': 'bio',
        'message': '请输入您的个人简介',
        'help_text': '连续两次按Enter结束输入'
    }
]

# 执行提示链
answers = inquirer.prompt(questions)

print(f"你好, {answers['name']}!")
if answers['likes_python']:
    print("太好了，我也喜欢Python!")
print(f"你最喜欢的语言是: {answers['favorite_lang']}")
print(f"你的个人简介:\n{answers['bio']}")
```

### 优雅处理中断

```python
from inquirer_console import inquirer, ExitPromptError

try:
    answers = inquirer.prompt([
        {
            'type': 'input',
            'name': 'name',
            'message': '你的名字是'
        }
    ])
    print(f"你好, {answers['name']}!")
except ExitPromptError:
    print("\n用户取消了操作，正在优雅退出...")
```

## 🔧 高级用法

### 验证和过滤

```python
from inquirer_console import Input

def validate_age(val):
    try:
        age = int(val)
        if age <= 0:
            return "年龄必须是正整数！"
        elif age > 120:
            return "年龄不能超过120岁！"
        return True
    except ValueError:
        return "请输入有效的数字！"

def filter_age(val):
    try:
        return int(val)
    except ValueError:
        return val

age = Input(
    message="你的年龄是",
    validate=validate_age,
    filter=filter_age
).prompt()

print(f"你的年龄是: {age} (类型: {type(age).__name__})")
```

### 多行文本输入

```python
from inquirer_console import Text

# 基本用法 - 连续两次按Enter结束输入
description = Text(
    message="请输入项目描述"
).prompt()

# 同时支持双回车和END文本结束
bio = Text(
    message="请输入您的个人简介",
    end_text="END"  # 除了双回车外，还可以通过输入END结束
).prompt()

# 带验证的多行文本输入
def validate_code(code):
    if "def main" not in code:
        return "代码必须包含main函数！"
    return True

code = Text(
    message="请输入一个Python代码示例",
    help_text="连续两次按Enter结束输入（代码必须包含main函数）",
    validate=validate_code
).prompt()
```

## 📚 API文档

详细的API文档请访问我们的[官方文档网站](https://example.com/docs)。

### 基础提示属性

所有提示类型都继承自 `BasePrompt` 并支持以下通用参数：

| 参数 | 类型 | 描述 |
|------|------|------|
| `message` | `str` | 向用户显示的提示消息 |
| `name` | `str` | 提示的名称，用于在answers字典中存储答案 |
| `default` | `Any` | 默认值，当用户未输入时使用 |
| `validate` | `Callable` | 验证函数，返回True或错误消息 |
| `filter` | `Callable` | 过滤函数，用于处理/转换用户输入 |

有关每种提示类型的特定参数，请参阅完整文档。

## 🧪 测试

### 运行测试

项目使用 pytest 进行测试。要运行测试，请执行以下命令：

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_input.py

# 运行特定测试用例
pytest tests/test_input.py::test_input_validation

# 运行并显示详细输出
pytest -v

# 生成覆盖率报告
pytest --cov=packages
```

### 添加新测试

添加新功能时，请同时添加相应的测试。测试文件应放在 `tests/` 目录中，并以 `test_` 开头。

```python
# tests/test_example.py
def test_new_feature():
    # 准备测试数据
    # 执行被测试的功能
    # 验证结果是否符合预期
    assert result == expected
```

### 测试覆盖率目标

我们的目标是保持至少 90% 的测试覆盖率。在提交 PR 前，请确保您的代码更改有适当的测试覆盖。

## 🤝 贡献指南

我们欢迎所有形式的贡献，无论是新功能、文档改进还是错误修复。请查看我们的[贡献指南](CONTRIBUTING.md)了解如何参与项目。

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/Eusen/inquirer_console.git
cd inquirer_console

# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Unix/macOS
# 或
venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest
```

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE) 进行许可。

## 💖 支持项目

如果你喜欢这个项目，可以通过以下方式支持我们：

- ⭐ 在 GitHub 上给我们点星
- 📣 在社交媒体上分享项目
- 🐛 提交 issue 或 PR
- 📝 完善文档

---

<p align="center">用 ❤️ 打造</p> 