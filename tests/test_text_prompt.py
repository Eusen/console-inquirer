"""
测试Text（多行文本输入提示）类
"""
from unittest.mock import patch

from packages import Text


class TestText:
    """测试Text类"""

    def test_init(self):
        """测试初始化"""
        # 基本初始化
        prompt = Text(message="测试消息")
        assert prompt.message == "测试消息"
        assert prompt.end_text is None
        assert prompt.help_text == "(连续两次按Enter结束输入，Ctrl+C取消)"
        assert prompt.default is None
        assert prompt.validate is None
        assert prompt.filter is None

        # 带参数初始化
        validate_func = lambda x: True
        filter_func = lambda x: x.strip()
        prompt = Text(
            message="测试消息",
            end_text="END",
            help_text="自定义帮助文本",
            default="默认文本",
            validate=validate_func,
            filter=filter_func
        )

        assert prompt.message == "测试消息"
        assert prompt.end_text == "END"
        assert prompt.help_text == "自定义帮助文本"
        assert prompt.default == "默认文本"
        assert prompt.validate == validate_func
        assert prompt.filter == filter_func

    def test_init_default_help_text(self):
        """测试默认帮助文本生成"""
        # 无end_text时的默认帮助文本
        prompt = Text(message="测试消息")
        assert prompt.help_text == "(连续两次按Enter结束输入，Ctrl+C取消)"

        # 有end_text时的默认帮助文本
        prompt = Text(message="测试消息", end_text="END")
        assert prompt.help_text == "(连续两次按Enter结束输入，或输入END单独一行结束输入，Ctrl+C取消)"

    @patch('builtins.input')
    def test_prompt_basic(self, mock_input, mock_stdout):
        """测试基本多行文本输入"""
        # 模拟用户输入：三行文本后连续两个空行
        mock_input.side_effect = ["第一行", "第二行", "第三行", "", ""]

        prompt = Text(message="测试消息")
        result = prompt._prompt()

        # 验证返回了正确的多行文本
        assert result == "第一行\n第二行\n第三行"

    @patch('builtins.input')
    def test_prompt_with_default(self, mock_input, mock_stdout):
        """测试带默认值的多行文本输入"""
        # 模拟用户直接按回车使用默认值
        mock_input.return_value = ""

        prompt = Text(message="测试消息", default="默认多行\n文本")
        result = prompt._prompt()

        # 验证返回了默认值
        assert result == "默认多行\n文本"

    @patch('builtins.input')
    def test_prompt_override_default(self, mock_input, mock_stdout):
        """测试覆盖默认值的多行文本输入"""
        # 模拟用户输入新内容而不使用默认值
        mock_input.side_effect = ["用户输入的第一行", "用户输入的第二行", "", ""]

        prompt = Text(message="测试消息", default="默认多行\n文本")
        result = prompt._prompt()

        # 验证返回了用户输入的内容
        assert result == "用户输入的第一行\n用户输入的第二行"

    @patch('builtins.input')
    def test_prompt_with_end_text(self, mock_input, mock_stdout):
        """测试使用结束标记文本结束输入"""
        # 模拟用户输入：两行文本后输入结束标记
        mock_input.side_effect = ["第一行", "第二行", "END"]

        prompt = Text(message="测试消息", end_text="END")
        result = prompt._prompt()

        # 验证返回了正确的多行文本（不包含结束标记）
        assert result == "第一行\n第二行"

    @patch('builtins.input')
    def test_prompt_validation(self, mock_input, mock_stdout):
        """测试多行文本验证"""
        # 模拟用户输入序列：首先是无效文本，然后是有效文本
        mock_input.side_effect = [
            "无效文本第一行", "无效文本第二行", "", "",  # 第一次输入（无效）
            "有效文本第一行", "需要包含关键词", "", ""  # 第二次输入（有效）
        ]

        # 定义验证函数，要求文本包含特定关键词
        def validate_func(text):
            if "关键词" not in text:
                return "文本必须包含'关键词'！"
            return True

        prompt = Text(message="测试消息", validate=validate_func)
        result = prompt._prompt()

        # 验证返回了有效文本
        assert result == "有效文本第一行\n需要包含关键词"

    @patch('builtins.input')
    def test_prompt_filter(self, mock_input, mock_stdout):
        """测试多行文本过滤"""
        # 模拟用户输入
        mock_input.side_effect = ["  有空格的第一行  ", "  有空格的第二行  ", "", ""]

        # 定义过滤函数，去除每行文本首尾的空格
        def filter_func(text):
            return "\n".join(line.strip() for line in text.split("\n"))

        prompt = Text(message="测试消息", filter=filter_func)
        result = prompt._prompt()

        # 验证返回的是过滤后的文本
        assert result == "有空格的第一行\n有空格的第二行"

    @patch('builtins.input')
    def test_prompt_filter_exception(self, mock_input, mock_stdout):
        """测试过滤器异常处理"""
        # 模拟用户输入序列：首先是会导致异常的输入，然后是正常输入
        mock_input.side_effect = [
            "异常文本", "", "",  # 第一次输入（会引发异常）
            "正常文本", "", ""  # 第二次输入（正常）
        ]

        # 定义会引发异常的过滤器函数
        def filter_func(text):
            if text == "异常文本":
                raise ValueError("过滤过程中出错")
            return text

        prompt = Text(message="测试消息", filter=filter_func)
        result = prompt._prompt()

        # 验证返回了第二次输入的文本
        assert result == "正常文本"

    @patch('builtins.input')
    def test_prompt_validation_exception(self, mock_input, mock_stdout):
        """测试验证异常处理"""
        # 模拟用户输入序列：首先是会导致异常的输入，然后是正常输入
        mock_input.side_effect = [
            "异常文本", "", "",  # 第一次输入（会引发异常）
            "正常文本", "", ""  # 第二次输入（正常）
        ]

        # 定义会引发异常的验证函数
        def validate_func(text):
            if text == "异常文本":
                raise Exception("验证过程中出错")
            return True

        prompt = Text(message="测试消息", validate=validate_func)
        result = prompt._prompt()

        # 验证返回了第二次输入的文本
        assert result == "正常文本"
