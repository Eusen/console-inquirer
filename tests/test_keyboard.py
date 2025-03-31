"""
测试键盘输入工具模块
"""
import os
import pytest
from unittest.mock import patch

from inquirer_console.utils import keyboard

class TestKeyboard:
    """测试键盘输入工具模块"""

    @patch('os.name', 'nt')  # 模拟Windows环境
    @patch('msvcrt.kbhit')
    @patch('msvcrt.getch')
    def test_get_key_windows(self, mock_getch, mock_kbhit):
        """测试Windows环境下的get_key函数"""
        # 导入新的键盘模块，以确保使用模拟的环境变量
        import sys
        if 'inquirer_console.utils.keyboard' in sys.modules:
            del sys.modules['inquirer_console.utils.keyboard']

        # 模拟无按键输入
        mock_kbhit.return_value = False
        assert keyboard.get_key() == ""

        # 模拟常规按键输入
        mock_kbhit.return_value = True
        mock_getch.return_value = b'a'
        assert keyboard.get_key() == "a"

        # 模拟Enter键
        mock_getch.return_value = b'\r'
        assert keyboard.get_key() == "\r"

        # 模拟上箭头键
        mock_getch.side_effect = [b'\xe0', b'H']
        assert keyboard.get_key() == "UP"

        # 模拟下箭头键
        mock_getch.side_effect = [b'\xe0', b'P']
        assert keyboard.get_key() == "DOWN"

        # 模拟右箭头键
        mock_getch.side_effect = [b'\xe0', b'M']
        assert keyboard.get_key() == "RIGHT"

        # 模拟左箭头键
        mock_getch.side_effect = [b'\xe0', b'K']
        assert keyboard.get_key() == "LEFT"

    @patch('os.name', 'nt')  # 模拟Windows环境
    @patch('msvcrt.getch')
    def test_wait_for_key_windows(self, mock_getch):
        """测试Windows环境下的wait_for_key函数"""
        # 导入新的键盘模块，以确保使用模拟的环境变量
        import sys
        if 'inquirer_console.utils.keyboard' in sys.modules:
            del sys.modules['inquirer_console.utils.keyboard']

        # 模拟常规按键输入
        mock_getch.return_value = b'a'
        assert keyboard.wait_for_key() == "a"

        # 模拟Enter键
        mock_getch.return_value = b'\r'
        assert keyboard.wait_for_key() == "\r"

        # 模拟上箭头键
        mock_getch.side_effect = [b'\xe0', b'H']
        assert keyboard.wait_for_key() == "UP"

    @pytest.mark.skipif(os.name == 'nt', reason="仅在Unix环境下测试")
    @patch('sys.stdin')
    @patch('select.select')
    @patch('tty.setraw')
    def test_get_key_unix(self, mock_setraw, mock_select, mock_stdin):
        """测试Unix环境下的get_key函数"""
        # 确保测试在Unix环境下运行时执行此测试

        # 模拟无按键输入
        mock_select.return_value = ([], None, None)
        get_key = keyboard.get_key
        assert get_key() == ""

        # 模拟常规按键输入
        mock_select.return_value = ([mock_stdin], None, None)
        mock_stdin.read.return_value = "a"
        assert get_key() == "a"

        # 模拟上箭头键
        mock_stdin.read.side_effect = ["\x1b", "[A"]
        assert get_key() == "UP"

        # 模拟下箭头键
        mock_stdin.read.side_effect = ["\x1b", "[B"]
        assert get_key() == "DOWN"

        # 模拟右箭头键
        mock_stdin.read.side_effect = ["\x1b", "[C"]
        assert get_key() == "RIGHT"

        # 模拟左箭头键
        mock_stdin.read.side_effect = ["\x1b", "[D"]
        assert get_key() == "LEFT"

    @pytest.mark.skipif(os.name == 'nt', reason="仅在Unix环境下测试")
    @patch('sys.stdin')
    @patch('tty.setraw')
    def test_wait_for_key_unix(self, mock_setraw, mock_stdin):
        """测试Unix环境下的wait_for_key函数"""
        # 确保测试在Unix环境下运行时执行此测试

        # 模拟常规按键输入
        mock_stdin.read.return_value = "a"
        wait_for_key = keyboard.wait_for_key
        assert wait_for_key() == "a"

        # 模拟上箭头键
        mock_stdin.read.side_effect = ["\x1b", "[A"]
        assert wait_for_key() == "UP"
