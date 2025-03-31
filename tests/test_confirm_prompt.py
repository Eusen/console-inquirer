"""
测试Confirm（确认提示）类
"""
from inquirer_console import Confirm


class TestConfirm:
    """测试Confirm类"""

    def test_init(self):
        """测试初始化"""
        # 默认值为True的初始化
        prompt = Confirm(message="测试消息")
        assert prompt.message == "测试消息"
        assert prompt.default is True

        # 显式设置默认值为False的初始化
        prompt = Confirm(message="测试消息", default=False)
        assert prompt.message == "测试消息"
        assert prompt.default is False

    def test_prompt_yes_input(self, mock_stdout, mock_input):
        """测试用户输入'是'的情况"""
        # 测试各种表示"是"的输入
        yes_inputs = ["y", "Y", "yes", "YES", "是", "1", "true", "True"]
        
        for yes_input in yes_inputs:
            mock_input.return_value = yes_input
            
            prompt = Confirm(message="测试消息", default=False)
            result = prompt._prompt()
            
            # 验证返回True
            assert result is True

    def test_prompt_no_input(self, mock_stdout, mock_input):
        """测试用户输入'否'的情况"""
        # 测试各种表示"否"的输入
        no_inputs = ["n", "N", "no", "NO", "否", "0", "false", "False"]
        
        for no_input in no_inputs:
            mock_input.return_value = no_input
            
            prompt = Confirm(message="测试消息", default=True)
            result = prompt._prompt()
            
            # 验证返回False
            assert result is False

    def test_prompt_empty_input(self, mock_stdout, mock_input):
        """测试用户输入为空的情况（使用默认值）"""
        # 模拟用户直接按回车（空输入）
        mock_input.return_value = ""
        
        # 测试默认值为True的情况
        prompt = Confirm(message="测试消息", default=True)
        result = prompt._prompt()
        
        # 验证返回了默认值True
        assert result is True
        
        # 测试默认值为False的情况
        prompt = Confirm(message="测试消息", default=False)
        result = prompt._prompt()
        
        # 验证返回了默认值False
        assert result is False

    def test_prompt_invalid_input(self, mock_stdout, mock_input):
        """测试用户输入无效值的情况"""
        # 模拟用户输入顺序：首先输入无效值，然后输入有效值
        mock_input.side_effect = ["invalid", "y"]
        
        prompt = Confirm(message="测试消息")
        result = prompt._prompt()
        
        # 验证最终返回了有效值（第二次输入的结果）
        assert result is True 