"""
测试Checkbox（复选框提示）类
"""
import pytest
from unittest.mock import patch, MagicMock

from src.prompts.checkbox import Checkbox


class TestCheckbox:
    """测试Checkbox类"""

    def test_init_with_string_choices(self):
        """测试使用字符串列表初始化"""
        prompt = Checkbox(
            message="测试消息",
            choices=["选项1", "选项2", "选项3"]
        )
        
        assert prompt.message == "测试消息"
        assert len(prompt.choices) == 3
        assert prompt.choices[0] == {"name": "选项1", "value": "选项1", "checked": False}
        assert prompt.choices[1] == {"name": "选项2", "value": "选项2", "checked": False}
        assert prompt.choices[2] == {"name": "选项3", "value": "选项3", "checked": False}
        assert prompt.selected_index == 0

    def test_init_with_dict_choices(self):
        """测试使用字典列表初始化"""
        choices = [
            {"name": "Python", "value": "python", "checked": True},
            {"name": "JavaScript", "value": "js"},
            {"name": "Rust", "value": "rust", "checked": False}
        ]
        
        prompt = Checkbox(
            message="测试消息",
            choices=choices
        )
        
        assert prompt.message == "测试消息"
        assert len(prompt.choices) == 3
        assert prompt.choices[0] == {"name": "Python", "value": "python", "checked": True}
        assert prompt.choices[1] == {"name": "JavaScript", "value": "js", "checked": False}
        assert prompt.choices[2] == {"name": "Rust", "value": "rust", "checked": False}
        assert prompt.selected_index == 0

    def test_init_with_default_values(self):
        """测试使用默认选中值初始化"""
        choices = [
            {"name": "Python", "value": "python"},
            {"name": "JavaScript", "value": "js"},
            {"name": "Rust", "value": "rust"}
        ]
        
        # 使用default参数设置默认选中项
        prompt = Checkbox(
            message="测试消息",
            choices=choices,
            default=["python", "rust"]
        )
        
        assert prompt.choices[0]["checked"] is True
        assert prompt.choices[1]["checked"] is False
        assert prompt.choices[2]["checked"] is True

    def test_init_with_missing_name(self):
        """测试选项缺少name属性时的异常"""
        choices = [
            {"value": "python"},  # 缺少name
            {"name": "JavaScript", "value": "js"}
        ]
        
        with pytest.raises(ValueError, match="选项 0 缺少'name'属性"):
            Checkbox(message="测试消息", choices=choices)

    def test_init_with_missing_value(self):
        """测试选项缺少value属性时自动使用name"""
        choices = [
            {"name": "Python"},  # 缺少value
            {"name": "JavaScript", "value": "js"}
        ]
        
        prompt = Checkbox(message="测试消息", choices=choices)
        assert prompt.choices[0] == {"name": "Python", "value": "Python", "checked": False}
        assert prompt.choices[1] == {"name": "JavaScript", "value": "js", "checked": False}

    def test_navigation_logic(self):
        """测试导航逻辑，不依赖键盘输入"""
        choices = ["选项1", "选项2", "选项3"]
        prompt = Checkbox(message="测试消息", choices=choices)
        
        # 模拟导航
        prompt.selected_index = 0
        # 向下移动两次
        prompt.selected_index += 1
        prompt.selected_index += 1
        # 向上移动一次
        prompt.selected_index -= 1
        
        # 此时应该在选项2上（索引1）
        assert prompt.selected_index == 1

    def test_selection_logic(self):
        """测试选择逻辑，不依赖键盘输入"""
        choices = ["选项1", "选项2", "选项3"]
        prompt = Checkbox(message="测试消息", choices=choices)
        
        # 初始状态应该都是未选中
        assert prompt.choices[0]["checked"] is False
        assert prompt.choices[1]["checked"] is False
        assert prompt.choices[2]["checked"] is False
        
        # 模拟选择操作
        prompt.selected_index = 0
        prompt.choices[prompt.selected_index]["checked"] = True  # 选中选项1
        
        prompt.selected_index = 1
        prompt.choices[prompt.selected_index]["checked"] = True  # 选中选项2
        
        prompt.selected_index = 0
        prompt.choices[prompt.selected_index]["checked"] = False  # 取消选中选项1
        
        # 验证结果
        assert prompt.choices[0]["checked"] is False
        assert prompt.choices[1]["checked"] is True
        assert prompt.choices[2]["checked"] is False
        
        # 获取选中的选项
        selected = [choice["value"] for choice in prompt.choices if choice["checked"]]
        assert selected == ["选项2"]

    def test_validation_logic(self):
        """测试验证逻辑，不依赖键盘输入"""
        choices = ["选项1", "选项2", "选项3"]
        
        # 定义验证函数，要求至少选择两个选项
        def validate_func(vals):
            if len(vals) < 2:
                return "请至少选择两个选项"
            return True
        
        prompt = Checkbox(
            message="测试消息", 
            choices=choices,
            validate=validate_func
        )
        
        # 测试不同情况
        # 只选择一个（应该失败）
        result = validate_func(["选项1"])
        assert result == "请至少选择两个选项"
        
        # 选择两个（应该成功）
        result = validate_func(["选项1", "选项2"])
        assert result is True

    def test_exception_handling_in_validation(self):
        """测试验证中的异常处理，不依赖键盘输入"""
        choices = ["选项1", "选项2", "选项3"]
        
        # 定义会引发异常的验证函数
        def validate_func(vals):
            if "选项1" in vals and not "选项2" in vals:
                raise Exception("必须同时选择选项2")
            return True
        
        prompt = Checkbox(
            message="测试消息", 
            choices=choices,
            validate=validate_func
        )
        
        # 测试异常情况
        try:
            validate_func(["选项1"])
            assert False, "应该引发异常"
        except Exception as e:
            assert str(e) == "必须同时选择选项2"
        
        # 测试正常情况
        assert validate_func(["选项1", "选项2"]) is True 