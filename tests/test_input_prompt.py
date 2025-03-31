"""
测试Input（输入提示）类
"""
from packages import Input


class TestInput:
    """测试Input类"""

    def test_init(self):
        """测试初始化"""
        # 默认初始化
        prompt = Input(message="测试消息")
        assert prompt.message == "测试消息"
        assert prompt.default is None
        assert prompt.validate is None
        assert prompt.filter is None
        assert prompt.transformer is None

        # 带参数的初始化
        def validate_func(val):
            return True

        def filter_func(val):
            return val

        def transformer_func(val):
            return val

        prompt = Input(
            message="测试消息",
            default="默认值",
            validate=validate_func,
            filter=filter_func,
            transformer=transformer_func
        )
        assert prompt.message == "测试消息"
        assert prompt.default == "默认值"
        assert prompt.validate == validate_func
        assert prompt.filter == filter_func
        assert prompt.transformer == transformer_func

    def test_prompt_basic(self, mock_stdout, mock_input):
        """测试基本提示功能"""
        # 模拟用户输入"测试输入"
        mock_input.return_value = "测试输入"

        prompt = Input(message="测试消息")
        result = prompt._prompt()

        # 验证返回了用户输入
        assert result == "测试输入"

    def test_prompt_default(self, mock_stdout, mock_input):
        """测试默认值功能"""
        # 模拟用户直接按回车（空输入）
        mock_input.return_value = ""

        prompt = Input(message="测试消息", default="默认值")
        result = prompt._prompt()

        # 验证返回了默认值
        assert result == "默认值"

    def test_prompt_filter(self, mock_stdout, mock_input):
        """测试过滤器功能"""
        # 模拟用户输入"test"
        mock_input.return_value = "test"

        # 定义过滤器函数将输入转为大写
        def filter_func(val):
            return val.upper()

        prompt = Input(message="测试消息", filter=filter_func)
        result = prompt._prompt()

        # 验证返回的是过滤后的值
        assert result == "TEST"

    def test_prompt_filter_exception(self, mock_stdout, mock_input):
        """测试过滤器异常处理"""
        # 模拟用户输入的顺序：首先输入会导致异常的值，然后输入正常值
        mock_input.side_effect = ["invalid", "valid"]

        # 定义会引发异常的过滤器函数
        def filter_func(val):
            if val == "invalid":
                raise ValueError("无效输入")
            return val

        prompt = Input(message="测试消息", filter=filter_func)
        result = prompt._prompt()

        # 验证返回了第二次输入的值
        assert result == "valid"

    def test_prompt_validate(self, mock_stdout, mock_input):
        """测试验证功能"""
        # 模拟用户输入顺序：首先输入无效值，然后输入有效值
        mock_input.side_effect = ["", "有效输入"]

        # 定义验证函数
        def validate_func(val):
            if not val:
                return "输入不能为空"
            return True

        prompt = Input(message="测试消息", validate=validate_func)
        result = prompt._prompt()

        # 验证返回了第二次输入的值
        assert result == "有效输入"

    def test_prompt_validate_exception(self, mock_stdout, mock_input):
        """测试验证异常处理"""
        # 模拟用户输入顺序：首先输入会导致异常的值，然后输入正常值
        mock_input.side_effect = ["exception", "valid"]

        # 定义会引发异常的验证函数
        def validate_func(val):
            if val == "exception":
                raise Exception("验证过程中出错")
            return True

        prompt = Input(message="测试消息", validate=validate_func)
        result = prompt._prompt()

        # 验证返回了第二次输入的值
        assert result == "valid"
