"""
pytest配置文件，包含通用测试夹具
"""
import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# 确保src目录在Python路径中
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def mock_stdout():
    """模拟标准输出"""
    mock_out = MagicMock()
    with patch("sys.stdout", mock_out):
        yield mock_out


@pytest.fixture
def mock_stdin():
    """模拟标准输入"""
    with patch("sys.stdin") as mock_in:
        yield mock_in


@pytest.fixture
def mock_input():
    """模拟input函数"""
    with patch("builtins.input") as mock_input_func:
        yield mock_input_func


@pytest.fixture
def sample_choices():
    """返回示例选项列表"""
    return [
        {"name": "Python", "value": "python"},
        {"name": "JavaScript", "value": "js"},
        {"name": "Rust", "value": "rust"},
    ]
