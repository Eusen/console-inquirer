"""
整合测试：测试inquirer链式调用API
"""
import pytest
from unittest.mock import patch, MagicMock

from src import inquirer, ExitPromptError


class TestInquirerIntegration:
    """测试inquirer整合功能"""

    @patch('src.prompts.input.Input._prompt')
    @patch('src.prompts.confirm.Confirm._prompt')
    @patch('src.prompts.select.Select._prompt')
    def test_prompt_chain(self, mock_list_prompt, mock_confirm_prompt, mock_input_prompt):
        """测试提示链式调用"""
        # 设置各个提示类的模拟返回值
        mock_input_prompt.return_value = "测试用户"
        mock_confirm_prompt.return_value = True
        mock_list_prompt.return_value = "python"
        
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
            }
        ]
        
        # 执行提示链
        answers = inquirer.prompt(questions)
        
        # 验证结果
        assert answers == {
            'name': '测试用户',
            'likes_python': True,
            'favorite_lang': 'python'
        }
        
        # 验证每个提示类都被调用了一次
        mock_input_prompt.assert_called_once()
        mock_confirm_prompt.assert_called_once()
        mock_list_prompt.assert_called_once()

    def test_prompt_chain_with_all_types(self):
        """测试所有提示类型的链式调用"""
        # 创建所有提示类型的模拟
        with patch('src.prompts.input.Input._prompt') as mock_input, \
             patch('src.prompts.confirm.Confirm._prompt') as mock_confirm, \
             patch('src.prompts.select.Select._prompt') as mock_list, \
             patch('src.prompts.checkbox.Checkbox._prompt') as mock_checkbox, \
             patch('src.prompts.password.Password._prompt') as mock_password, \
             patch('src.prompts.text.Text._prompt') as mock_text:
            
            # 设置各个提示类的模拟返回值
            mock_input.return_value = "测试用户"
            mock_confirm.return_value = True
            mock_list.return_value = "python"
            mock_checkbox.return_value = ["python", "js"]
            mock_password.return_value = "secure_password"
            mock_text.return_value = "这是一段多行文本\n测试示例"
            
            # 定义包含所有提示类型的问题列表
            questions = [
                {'type': 'input', 'name': 'name', 'message': '姓名'},
                {'type': 'confirm', 'name': 'confirm', 'message': '确认'},
                {'type': 'list', 'name': 'list', 'message': '列表', 'choices': ['a', 'b']},
                {'type': 'checkbox', 'name': 'checkbox', 'message': '复选框', 'choices': ['a', 'b']},
                {'type': 'password', 'name': 'password', 'message': '密码'},
                {'type': 'text', 'name': 'text', 'message': '文本'}
            ]
            
            # 执行提示链
            answers = inquirer.prompt(questions)
            
            # 验证结果包含所有问题的答案
            assert set(answers.keys()) == {'name', 'confirm', 'list', 'checkbox', 'password', 'text'}
            assert answers['name'] == "测试用户"
            assert answers['confirm'] is True
            assert answers['list'] == "python"
            assert answers['checkbox'] == ["python", "js"]
            assert answers['password'] == "secure_password"
            assert answers['text'] == "这是一段多行文本\n测试示例"

    def test_exit_prompt_propagation(self):
        """测试退出提示异常的传播"""
        # 创建会引发ExitError的模拟
        with patch('src.prompts.input.Input.prompt', side_effect=ExitPromptError()):
            # 定义问题列表
            questions = [
                {'type': 'input', 'name': 'name', 'message': '姓名'},
                {'type': 'confirm', 'name': 'confirm', 'message': '确认'}
            ]
            
            # 验证异常被正确传播
            with pytest.raises(ExitPromptError):
                inquirer.prompt(questions)

    def test_unknown_prompt_type(self):
        """测试未知提示类型处理"""
        # 定义包含未知提示类型的问题
        questions = [
            {'type': 'unknown_type', 'name': 'test', 'message': '测试'}
        ]
        
        # 验证引发了正确的异常
        with pytest.raises(ValueError, match="未知的提示类型: unknown_type"):
            inquirer.prompt(questions)

    def test_register_custom_prompt(self):
        """测试注册自定义提示类型"""
        # 创建自定义提示类的模拟
        mock_custom_prompt = MagicMock()
        mock_custom_prompt.return_value.prompt.return_value = "自定义结果"
        
        # 注册自定义提示类型
        inquirer.register_prompt('custom', mock_custom_prompt)
        
        # 使用自定义提示类型
        questions = [
            {'type': 'custom', 'name': 'custom_answer', 'message': '自定义提示'}
        ]
        
        answers = inquirer.prompt(questions)
        
        # 验证结果
        assert answers['custom_answer'] == "自定义结果"
        
        # 验证自定义提示类被正确调用
        mock_custom_prompt.assert_called_once_with(name='custom_answer', message='自定义提示') 