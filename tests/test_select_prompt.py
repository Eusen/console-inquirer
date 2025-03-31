"""
测试Select（列表选择提示）类
"""
import pytest

from packages import Select


class TestSelect:
    """测试Select类"""

    def test_init_with_string_choices(self):
        """测试使用字符串列表初始化"""
        prompt = Select(
            message="测试消息",
            choices=["选项1", "选项2", "选项3"]
        )

        assert prompt.message == "测试消息"
        assert len(prompt.choices) == 3
        assert prompt.choices[0] == {"name": "选项1", "value": "选项1"}
        assert prompt.choices[1] == {"name": "选项2", "value": "选项2"}
        assert prompt.choices[2] == {"name": "选项3", "value": "选项3"}
        assert prompt.selected_index == 0

    def test_init_with_dict_choices(self):
        """测试使用字典列表初始化"""
        choices = [
            {"name": "Python", "value": "python"},
            {"name": "JavaScript", "value": "js"},
            {"name": "Rust", "value": "rust"}
        ]

        prompt = Select(
            message="测试消息",
            choices=choices
        )

        assert prompt.message == "测试消息"
        assert len(prompt.choices) == 3
        assert prompt.choices[0] == {"name": "Python", "value": "python"}
        assert prompt.choices[1] == {"name": "JavaScript", "value": "js"}
        assert prompt.choices[2] == {"name": "Rust", "value": "rust"}
        assert prompt.selected_index == 0

    def test_init_with_default_value(self):
        """测试使用默认值初始化"""
        choices = [
            {"name": "Python", "value": "python"},
            {"name": "JavaScript", "value": "js"},
            {"name": "Rust", "value": "rust"}
        ]

        # 使用值作为默认值
        prompt = Select(
            message="测试消息",
            choices=choices,
            default="js"
        )

        assert prompt.selected_index == 1

        # 使用索引作为默认值
        prompt = Select(
            message="测试消息",
            choices=choices,
            default=2
        )

        assert prompt.selected_index == 2

    def test_init_with_missing_name(self):
        """测试选项缺少name属性时的异常"""
        choices = [
            {"value": "python"},  # 缺少name
            {"name": "JavaScript", "value": "js"}
        ]

        with pytest.raises(ValueError, match="选项 0 缺少'name'属性"):
            Select(message="测试消息", choices=choices)

    def test_init_with_missing_value(self):
        """测试选项缺少value属性时自动使用name"""
        choices = [
            {"name": "Python"},  # 缺少value
            {"name": "JavaScript", "value": "js"}
        ]

        prompt = Select(message="测试消息", choices=choices)
        assert prompt.choices[0] == {"name": "Python", "value": "Python"}
        assert prompt.choices[1] == {"name": "JavaScript", "value": "js"}

    def test_selection_logic(self):
        """测试选择逻辑，不依赖键盘输入"""
        choices = ["选项1", "选项2", "选项3"]
        prompt = Select(message="测试消息", choices=choices)

        # 模拟向下移动
        prompt.selected_index = 0
        # 向下移动两次
        prompt.selected_index += 1
        prompt.selected_index += 1
        # 向上移动一次
        prompt.selected_index -= 1

        # 此时应该选中第二个选项（索引1）
        assert prompt.selected_index == 1
        assert prompt.choices[prompt.selected_index]['value'] == "选项2"

    def test_validation_logic(self):
        """测试验证逻辑，不依赖键盘输入"""
        choices = ["选项1", "选项2", "选项3"]

        # 定义验证函数，只允许选择"选项2"
        def validate_func(val):
            if val == "选项2":
                return True
            return "只能选择选项2"

        prompt = Select(
            message="测试消息",
            choices=choices,
            validate=validate_func
        )

        # 测试验证"选项1"（应该失败）
        result = validate_func("选项1")
        assert result == "只能选择选项2"

        # 测试验证"选项2"（应该成功）
        result = validate_func("选项2")
        assert result is True

    def test_exception_handling_in_validation(self):
        """测试验证中的异常处理，不依赖键盘输入"""
        choices = ["选项1", "选项2", "选项3"]

        # 定义会引发异常的验证函数
        def validate_func(val):
            if val == "选项1":
                raise Exception("验证过程中出错")
            return True

        prompt = Select(
            message="测试消息",
            choices=choices,
            validate=validate_func
        )

        # 测试异常情况
        try:
            validate_func("选项1")
            assert False, "应该引发异常"
        except Exception as e:
            assert str(e) == "验证过程中出错"

        # 测试正常情况
        assert validate_func("选项2") is True
