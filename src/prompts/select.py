"""
列表选择提示模块，用于从选项列表中选择一个选项。
"""
import sys
import time
from typing import List, Dict, Any, Optional, Union, Callable

from ..prompt import BasePrompt
from src.utils.keyboard import get_key


class Select(BasePrompt[Any]):
    """
    列表选择提示类，用于从选项列表中选择一个选项。

    #### Args:
    - message: 向用户显示的提示消息
    - choices: 可选项列表，每个选项可以是字符串或者包含name和value的字典
    - default: 默认选中的选项，可以是值或索引
    - validate: 用于验证用户选择的函数，返回布尔值或错误消息
    - **kwargs: 额外的参数
    
    示例:
    ```python
    from inquirer_console import Select

    choices = [
        {'name': 'Python', 'value': 'python'},
        {'name': 'JavaScript', 'value': 'js'},
        {'name': 'Rust', 'value': 'rust'}
    ]

    favorite_lang = Select(
        message="你最喜欢的编程语言是?",
        choices=choices
    ).prompt()

    print(f"你选择了: {favorite_lang}")
    ```
    """
    
    def __init__(self, message: str, choices: List[Union[str, Dict[str, Any]]],
                 default: Optional[Any] = None,
                 validate: Optional[Callable[[Any], Union[bool, str]]] = None,
                 **kwargs):
        """
        初始化列表选择提示。
        """
        super().__init__(message, default=default, **kwargs)
        self.validate = validate
        
        # 标准化选项列表
        self.choices = []
        for i, choice in enumerate(choices):
            if isinstance(choice, str):
                self.choices.append({'name': choice, 'value': choice})
            else:
                if 'name' not in choice:
                    raise ValueError(f"选项 {i} 缺少'name'属性")
                if 'value' not in choice:
                    choice['value'] = choice['name']
                self.choices.append(choice)
        
        # 找到默认选项的索引
        self.selected_index = 0
        if default is not None:
            for i, choice in enumerate(self.choices):
                if (isinstance(default, int) and i == default) or \
                   choice['value'] == default:
                    self.selected_index = i
                    break
    
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
        # 先显示提示信息
        sys.stdout.write(f"{self.message}\n")
        
        # 显示选项列表
        for i, choice in enumerate(self.choices):
            prefix = ">" if i == self.selected_index else " "
            sys.stdout.write(f"{prefix} {choice['name']}\n")
        
        sys.stdout.flush()
    
    def _prompt(self) -> Any:
        """
        执行提示并返回用户选择的选项值。
        
        Returns:
            用户选择的选项的值
        """
        # 渲染初始选项列表
        self._render_choices()
        
        while True:
            key = get_key()
            
            if key == 'UP' and self.selected_index > 0:
                # 清除当前渲染
                self._clear_screen(len(self.choices) + 1)
                
                # 更新选中项并重新渲染
                self.selected_index -= 1
                self._render_choices()
                
            elif key == 'DOWN' and self.selected_index < len(self.choices) - 1:
                # 清除当前渲染
                self._clear_screen(len(self.choices) + 1)
                
                # 更新选中项并重新渲染
                self.selected_index += 1
                self._render_choices()
                
            elif key in ('\r', '\n'):  # Enter键
                # 清除当前渲染
                self._clear_screen(len(self.choices) + 1)
                
                selected_value = self.choices[self.selected_index]['value']
                
                # 验证选择
                if self.validate:
                    try:
                        validate_result = self.validate(selected_value)
                        if validate_result is not True:
                            if isinstance(validate_result, str):
                                sys.stdout.write(f"{validate_result}\n")
                            else:
                                sys.stdout.write("选择无效，请重试。\n")
                            # 重新渲染选项列表
                            self._render_choices()
                            continue
                    except Exception as e:
                        sys.stdout.write(f"验证错误: {str(e)}\n")
                        # 重新渲染选项列表
                        self._render_choices()
                        continue
                
                # 显示最终选择
                sys.stdout.write(f"{self.message} {self.choices[self.selected_index]['name']}\n")
                sys.stdout.flush()
                
                return selected_value
            
            # 为了避免CPU使用率过高，加入短暂的延迟
            time.sleep(0.1) 