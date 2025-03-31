"""
复选框提示模块，用于从选项列表中选择多个选项。
"""
import sys
import time
from typing import List, Dict, Any, Optional, Union, Callable

from ..prompt import BasePrompt
from src.utils.keyboard import get_key


class Checkbox(BasePrompt[List[Any]]):
    """
    复选框提示类，用于从选项列表中选择多个选项。

    #### Args:
    - message: 向用户显示的提示消息
    - choices: 可选项列表，每个选项可以是字符串或者包含name和value的字典
    - default: 默认选中的选项的值列表
    - validate: 用于验证用户选择的函数，返回布尔值或错误消息
    - **kwargs: 额外的参数
    
    #### 示例:
    ```python
    from inquirer_console import Checkbox

    choices = [
        {'name': 'Python', 'value': 'python'},
        {'name': 'JavaScript', 'value': 'js', 'checked': True},
        {'name': 'Rust', 'value': 'rust'}
    ]

    languages = Checkbox(
        message="选择你喜欢的编程语言",
        choices=choices
    ).prompt()

    for lang in languages:
        print(f"你选择了: {lang}")
    ```
    """

    def __init__(
            self,
            message: str,
            choices: List[Union[str, Dict[str, Any]]],
            default: Optional[List[Any]] = None,
            validate: Optional[Callable[[List[Any]], Union[bool, str]]] = None,
            **kwargs
    ):
        """
        初始化复选框提示。
        """
        super().__init__(message, default=default, **kwargs)
        self.validate = validate

        # 标准化选项列表
        self.choices = []
        for i, choice in enumerate(choices):
            if isinstance(choice, str):
                self.choices.append({
                    'name': choice,
                    'value': choice,
                    'checked': False
                })
            else:
                if 'name' not in choice:
                    raise ValueError(f"选项 {i} 缺少'name'属性")
                if 'value' not in choice:
                    choice['value'] = choice['name']
                if 'checked' not in choice:
                    choice['checked'] = False
                self.choices.append(choice)

        # 应用默认选中项
        if default is not None:
            for choice in self.choices:
                if choice['value'] in default:
                    choice['checked'] = True

        self.selected_index = 0

    def _clear_screen(self, num_lines: int):
        """
        清除屏幕上的指定行数。
        
        Args:
            num_lines: 要清除的行数
        """
        sys.stdout.write("\r")
        for _ in range(num_lines):
            sys.stdout.write("\033[K\033[A")  # 清除当前行并上移一行
        sys.stdout.write("\033[K")  # 清除最后一行
        sys.stdout.flush()

    def _render_choices(self):
        """渲染选项列表。"""
        # 显示提示信息和帮助文本
        sys.stdout.write(f"{self.message}\n")
        sys.stdout.write("(使用上下箭头选择，空格切换选中状态，Enter确认)\n")

        # 显示选项列表
        for i, choice in enumerate(self.choices):
            prefix = ">" if i == self.selected_index else " "
            checkbox = "[X]" if choice['checked'] else "[ ]"
            sys.stdout.write(f"{prefix} {checkbox} {choice['name']}\n")

        sys.stdout.flush()

    def _prompt(self) -> list[str | bool] | None:
        """
        执行提示并返回用户选择的选项值列表。
        
        Returns:
            用户选择的选项的值列表
        """
        # 渲染初始选项列表
        self._render_choices()

        while True:
            key = get_key()

            if key == 'UP' and self.selected_index > 0:
                # 清除当前渲染
                self._clear_screen(len(self.choices) + 2)  # +2是因为有提示行和帮助行

                # 更新选中项并重新渲染
                self.selected_index -= 1
                self._render_choices()

            elif key == 'DOWN' and self.selected_index < len(self.choices) - 1:
                # 清除当前渲染
                self._clear_screen(len(self.choices) + 2)

                # 更新选中项并重新渲染
                self.selected_index += 1
                self._render_choices()

            elif key == ' ':  # 空格键切换选中状态
                # 切换当前选项的选中状态
                self.choices[self.selected_index]['checked'] = not self.choices[self.selected_index]['checked']

                # 清除当前渲染并重新渲染
                self._clear_screen(len(self.choices) + 2)
                self._render_choices()

            elif key in ('\r', '\n'):  # Enter键
                # 获取所有选中的选项的值
                selected_values = [
                    choice['value'] for choice in self.choices if choice['checked']
                ]

                # 验证选择
                if self.validate:
                    try:
                        validate_result = self.validate(selected_values)
                        if validate_result is not True:
                            if isinstance(validate_result, str):
                                # 清除当前渲染
                                self._clear_screen(len(self.choices) + 2)
                                sys.stdout.write(f"{validate_result}\n")
                            else:
                                # 清除当前渲染
                                self._clear_screen(len(self.choices) + 2)
                                sys.stdout.write("选择无效，请重试。\n")
                            # 重新渲染选项列表
                            self._render_choices()
                            continue
                    except Exception as e:
                        # 清除当前渲染
                        self._clear_screen(len(self.choices) + 2)
                        sys.stdout.write(f"验证错误: {str(e)}\n")
                        # 重新渲染选项列表
                        self._render_choices()
                        continue

                # 清除当前渲染
                self._clear_screen(len(self.choices) + 2)

                # 显示最终选择
                selected_names = [
                    choice['name'] for choice in self.choices if choice['checked']
                ]
                sys.stdout.write(f"{self.message} {', '.join(selected_names)}\n")
                sys.stdout.flush()

                return selected_values

            # 为了避免CPU使用率过高，加入短暂的延迟
            time.sleep(0.1)
