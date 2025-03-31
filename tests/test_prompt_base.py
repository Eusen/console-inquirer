"""
测试Base类和ExitError异常
"""
import pytest
import signal
from unittest.mock import patch, MagicMock

from packages import BasePrompt, ExitPromptError


class TestBase:
    """测试Base基类"""

    class Test(BasePrompt):
        """实现测试用的具体提示类"""
        def _prompt(self):
            return self.default

    def test_init(self):
        """测试初始化"""
        prompt = self.Test(message="测试消息", name="test_name", default="默认值")
        assert prompt.message == "测试消息"
        assert prompt.name == "test_name"
        assert prompt.default == "默认值"

    def test_signal_handlers(self):
        """测试信号处理器设置和恢复"""
        original_handler = signal.getsignal(signal.SIGINT)
        prompt = self.Test(message="测试消息")
        
        # 确认设置了新的处理器
        assert signal.getsignal(signal.SIGINT) != original_handler
        
        # 调用prompt方法后应该恢复原始处理器
        prompt.prompt()
        assert signal.getsignal(signal.SIGINT) == original_handler

    def test_prompt_calls_abstract_method(self):
        """测试prompt方法调用抽象的_prompt方法"""
        prompt = self.Test(message="测试消息", default="测试值")
        result = prompt.prompt()
        assert result == "测试值"

    def test_exit_prompt_error(self):
        """测试 ExitPromptError 异常"""
        error = ExitPromptError()
        assert str(error) == "用户强制关闭了提示"
        
        custom_error = ExitPromptError("自定义错误信息")
        assert str(custom_error) == "自定义错误信息"

    def test_interrupt_handling(self):
        """测试中断处理"""
        prompt = self.Test(message="测试消息")
        
        # 模拟SIGINT信号处理器
        def simulate_sigint_handler():
            handler = signal.getsignal(signal.SIGINT)
            handler(signal.SIGINT, None)
        
        # 确认触发处理器会引发ExitPromptError
        with pytest.raises(ExitPromptError):
            with patch.object(prompt, '_prompt', side_effect=simulate_sigint_handler):
                prompt.prompt()


class TestInquirer:
    """测试Inquirer类"""
    
    def test_register_prompt(self):
        """测试注册提示类型"""
        from packages import Inquirer
        
        inquirer = Inquirer()
        mock_class = MagicMock()
        inquirer.register_prompt("test", mock_class)
        
        assert inquirer._prompts["test"] == mock_class
    
    def test_prompt_unknown_type(self):
        """测试使用未知提示类型"""
        from packages import Inquirer
        
        inquirer = Inquirer()
        
        with pytest.raises(ValueError, match="未知的提示类型"):
            inquirer.prompt([
                {
                    "type": "unknown_type",
                    "name": "test",
                    "message": "测试"
                }
            ])
    
    def test_prompt_chain(self):
        """测试提示链"""
        from packages import Inquirer
        
        # 创建模拟提示类
        mock_prompt = MagicMock()
        mock_prompt.return_value.prompt.return_value = "测试回答"
        
        inquirer = Inquirer()
        inquirer.register_prompt("test", mock_prompt)
        
        result = inquirer.prompt([
            {
                "type": "test",
                "name": "question1",
                "message": "测试问题1"
            },
            {
                "type": "test",
                "name": "question2",
                "message": "测试问题2"
            }
        ])
        
        assert result == {"question1": "测试回答", "question2": "测试回答"}
        assert mock_prompt.call_count == 2 