<div align="center">
  <p>
    <a href="https://github.com/Eusen/inquirer_console/blob/master/README.zh.md">中文</a> | 
    <a href="/">English</a>
  </p>
  
  <h1>🐣inquirer_console</h1>
  <p>An elegant interactive command line interface tool library</p>
  
  <p>
    <a href="https://github.com/Eusen/inquirer_console/blob/master/README.md#-installation"><strong>Installation</strong></a> •
    <a href="https://github.com/Eusen/inquirer_console/blob/master/README.md#-features"><strong>Features</strong></a> •
    <a href="https://github.com/Eusen/inquirer_console/blob/master/README.md#-usage-examples"><strong>Usage Examples</strong></a> •
    <a href="https://github.com/Eusen/inquirer_console/blob/master/README.md#-api-documentation"><strong>API Docs</strong></a> •
    <a href="https://github.com/Eusen/inquirer_console/blob/master/README.md#-contributing"><strong>Contributing</strong></a>
  </p>
  
  <p>
    <img alt="Python Version" src="https://img.shields.io/badge/Python-3.12%2B-blue?style=flat-square&logo=python">
    <img alt="License" src="https://img.shields.io/badge/License-MIT-green?style=flat-square">
    <img alt="PRs Welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square">
  </p>
</div>

## 📖 Introduction

inquirer_console is a Python implementation of [Inquirer.js](https://github.com/SBoudrias/Inquirer.js), providing a set of well-designed interactive command line interface components that allow developers to easily create beautiful, user-friendly command line applications.

## ✨ Features

- **Cross-platform compatibility** - Perfect support for Windows, macOS, and various Linux/Unix systems
- **Elegant interrupt handling** - Intelligent handling of Ctrl+C, ensuring a smooth user experience
- **Powerful input validation** - Easily validate user input through custom validate functions
- **Flexible data transformation** - Transform user input in real-time through filter functions
- **Chainable API** - Provides a fluent API similar to Inquirer.js, simplifying complex interactions
- **Fully type-annotated** - Comprehensive type hints to enhance development experience
- **Zero external dependencies** - Implemented with pure Python standard library, no additional installations required

## 🧩 Prompt Types

inquirer_console currently implements the following prompt types:

| Type | Description | Preview |
|------|-------------|---------|
| **Input** | Text input prompt | `> Please enter your name:` |
| **Confirm** | Confirmation prompt (yes/no) | `> Continue? (Y/n):` |
| **Select** | List selection prompt (single choice) | `> Select an option: ❯ Option1 ⬡ Option2 ⬡ Option3` |
| **Checkbox** | Checkbox prompt (multiple choice) | `> Select multiple options: ❯ [X] Option1 [ ] Option2 [X] Option3` |
| **Password** | Password input prompt | `> Please enter a password: ******` |
| **Text** | Multi-line text input prompt | `> Please enter a description: (Press Enter twice to finish)` |

## 🚀 Installation

Currently in development stage, you can install it via:

```bash
# Install from PyPI
pip install inquirer_console

# Install directly from GitHub
pip install git+https://github.com/Eusen/inquirer_console.git

# Or clone the repository and use
git clone https://github.com/Eusen/inquirer_console.git
cd inquirer_console
pip install -e .
```

## 📝 Usage Examples

### Using Each Prompt Type Individually

```python
from inquirer_console import Input, Confirm, Select, Checkbox, Password, Text

# Input prompt
name = Input(
    message="What is your name",
    validate=lambda val: True if val else "Name cannot be empty!"
).prompt()

# Confirm prompt
likes_python = Confirm(
    message="Do you like Python",
    default=True
).prompt()

# Select prompt
favorite_lang = Select(
    message="What is your favorite programming language",
    choices=[
        {'name': 'Python', 'value': 'python'},
        {'name': 'JavaScript', 'value': 'js'},
        {'name': 'Rust', 'value': 'rust'}
    ]
).prompt()

# Checkbox prompt
languages = Checkbox(
    message="Which programming languages do you use",
    choices=[
        {'name': 'Python', 'value': 'python', 'checked': True},
        {'name': 'JavaScript', 'value': 'js'},
        {'name': 'Rust', 'value': 'rust'}
    ]
).prompt()

# Password prompt
password = Password(
    message="Please enter a password",
    validate=lambda val: True if len(val) >= 6 else "Password must be at least 6 characters!"
).prompt()

# Multi-line text prompt (finish by pressing Enter twice)
description = Text(
    message="Please enter a project description"
).prompt()
```

### Using inquirer Chain Calls

```python
from inquirer_console import inquirer

# Define a select of questions
questions = [
    {
        'type': 'input',
        'name': 'name',
        'message': 'What is your name',
        'validate': lambda val: True if val else "Name cannot be empty!"
    },
    {
        'type': 'confirm',
        'name': 'likes_python',
        'message': 'Do you like Python',
        'default': True
    },
    {
        'type': 'select',
        'name': 'favorite_lang',
        'message': 'What is your favorite programming language',
        'choices': [
            {'name': 'Python', 'value': 'python'},
            {'name': 'JavaScript', 'value': 'js'},
            {'name': 'Rust', 'value': 'rust'}
        ]
    },
    {
        'type': 'text',
        'name': 'bio',
        'message': 'Please enter your bio',
        'help_text': 'Press Enter twice to finish input'
    }
]

# Execute the prompt chain
answers = inquirer.prompt(questions)

print(f"Hello, {answers['name']}!")
if answers['likes_python']:
    print("Great, I like Python too!")
print(f"Your favorite language is: {answers['favorite_lang']}")
print(f"Your bio:\n{answers['bio']}")
```

### Gracefully Handling Interruptions

```python
from inquirer_console import inquirer, ExitPromptError

try:
    answers = inquirer.prompt([
        {
            'type': 'input',
            'name': 'name',
            'message': 'What is your name'
        }
    ])
    print(f"Hello, {answers['name']}!")
except ExitPromptError:
    print("\nUser canceled the operation, gracefully exiting...")
```

## 🔧 Advanced Usage

### Validation and Filtering

```python
from inquirer_console import Input

def validate_age(val):
    try:
        age = int(val)
        if age <= 0:
            return "Age must be a positive integer!"
        elif age > 120:
            return "Age cannot exceed 120 years!"
        return True
    except ValueError:
        return "Please enter a valid number!"

def filter_age(val):
    try:
        return int(val)
    except ValueError:
        return val

age = Input(
    message="What is your age",
    validate=validate_age,
    filter=filter_age
).prompt()

print(f"Your age is: {age} (type: {type(age).__name__})")
```

### Multi-line Text Input

```python
from inquirer_console import Text

# Basic usage - finish by pressing Enter twice
description = Text(
    message="Please enter a project description"
).prompt()

# Supports both double Enter and END text to finish
bio = Text(
    message="Please enter your bio",
    end_text="END"  # Besides double Enter, can also finish by typing END
).prompt()

# Multi-line text input with validation
def validate_code(code):
    if "def main" not in code:
        return "Code must include a main function!"
    return True

code = Text(
    message="Please enter a Python code example",
    help_text="Press Enter twice to finish input (code must include main function)",
    validate=validate_code
).prompt()
```

## 📚 API Documentation

For detailed API documentation, please visit our [official documentation website](https://example.com/docs).

### Basic Prompt Properties

All prompt types inherit from `BasePrompt` and support the following common parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `message` | `str` | The prompt message displayed to the user |
| `name` | `str` | The name of the prompt, used to store the answer in the answers dictionary |
| `default` | `Any` | Default value, used when the user doesn't provide input |
| `validate` | `Callable` | Validation function, returns True or an error message |
| `filter` | `Callable` | Filter function, used to process/transform user input |

For specific parameters for each prompt type, please refer to the complete documentation.

## 🧪 Testing

### Running Tests

The project uses pytest for testing. To run tests, execute the following commands:

```bash
# Run all tests
pytest

# Run a specific test file
pytest tests/test_input.py

# Run a specific test case
pytest tests/test_input.py::test_input_validation

# Run with verbose output
pytest -v

# Generate coverage report
pytest --cov=packages
```

### Adding New Tests

When adding new features, please also add corresponding tests. Test files should be placed in the `tests/` directory and should start with `test_`.

```python
# tests/test_example.py
def test_new_feature():
    # Prepare test data
    # Execute the feature being tested
    # Verify the results meet expectations
    assert result == expected
```

### Test Coverage Goals

Our goal is to maintain at least 90% test coverage. Before submitting a PR, please ensure your code changes have adequate test coverage.

## 🤝 Contributing

We welcome all forms of contributions, whether they are new features, documentation improvements, or bug fixes. Please check our [contribution guidelines](CONTRIBUTING.md) to learn how to participate in the project.

### Development Environment Setup

```bash
# Clone the repository
git clone https://github.com/Eusen/inquirer_console.git
cd inquirer_console

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Unix/macOS
# or
venv\Scripts\activate  # Windows

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## 📄 License

This project is licensed under the [MIT License](https://github.com/Eusen/inquirer_console/blob/master/LICENSE).

## 💖 Support the Project

If you like this project, you can support us by:

- ⭐ Starring us on GitHub
- 📣 Sharing the project on social media
- 🐛 Submitting issues or PRs
- 📝 Improving documentation

---

<p align="center">Made with ❤️</p> 