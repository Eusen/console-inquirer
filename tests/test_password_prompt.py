"""
测试Password（密码输入提示）类
"""
from unittest.mock import patch

from packages import Password


class TestPassword:
    """测试Password类"""

    def test_init(self):
        """测试初始化"""
        # 默认初始化
        prompt = Password(message="测试消息")
        assert prompt.message == "测试消息"
        assert prompt.mask == "*"
        assert prompt.validate is None

        # 带参数初始化
        validate_func = lambda x: True if len(x) >= 6 else "密码太短"
        prompt = Password(
            message="测试消息",
            mask="#",
            validate=validate_func
        )

        assert prompt.message == "测试消息"
        assert prompt.mask == "#"
        assert prompt.validate == validate_func

        # 无掩码初始化
        prompt = Password(message="测试消息", mask=None)
        assert prompt.mask is None

    @patch('getpass.getpass')
    def test_prompt_with_mask(self, mock_getpass, mock_stdout):
        """测试带掩码的密码输入"""
        # 设置getpass模拟的返回值序列：字符-字符-字符-回车
        mock_getpass.side_effect = ["a", "b", "c", ""]

        prompt = Password(message="测试消息", mask="*")
        result = prompt._prompt()

        # 验证返回了正确的密码
        assert result == "abc"

    @patch('getpass.getpass')
    def test_prompt_without_mask(self, mock_getpass, mock_stdout):
        """测试无掩码的密码输入"""
        # 设置getpass模拟的返回值
        mock_getpass.return_value = "password123"

        prompt = Password(message="测试消息", mask=None)
        result = prompt._prompt()

        # 验证返回了正确的密码
        assert result == "password123"

    @patch('getpass.getpass')
    def test_prompt_validation(self, mock_getpass, mock_stdout):
        """测试密码验证"""
        # 设置getpass模拟的返回值序列：首先是短密码，然后是有效密码
        # 对于无掩码模式，直接返回密码
        mock_getpass.side_effect = ["short", "valid_password"]

        # 定义验证函数，要求密码至少6个字符
        def validate_func(val):
            if len(val) < 6:
                return "密码至少需要6个字符！"
            return True

        prompt = Password(
            message="测试消息",
            mask=None,
            validate=validate_func
        )

        result = prompt._prompt()

        # 验证返回了有效密码
        assert result == "valid_password"

    @patch('getpass.getpass')
    def test_prompt_validation_exception(self, mock_getpass, mock_stdout):
        """测试密码验证异常处理"""
        # 设置getpass模拟的返回值序列：首先是会引发异常的密码，然后是有效密码
        mock_getpass.side_effect = ["invalid", "valid_password"]

        # 定义会引发异常的验证函数
        def validate_func(val):
            if val == "invalid":
                raise Exception("验证过程中出错")
            return True

        prompt = Password(
            message="测试消息",
            mask=None,
            validate=validate_func
        )

        result = prompt._prompt()

        # 验证返回了有效密码
        assert result == "valid_password"
