"""
输入提示模块，用于获取用户的文本输入。
"""
import sys
from typing import Optional, Union, Callable

from ..prompt import BasePrompt


class Input(BasePrompt[str]):
    """
    输入提示类，用于获取用户的文本输入。

    #### Args:
    - message: 向用户显示的提示消息
    - default: 当用户未输入时的默认值
    - validate: 用于验证用户输入的函数，返回布尔值或错误消息
    - filter: 用于过滤/转换用户输入的函数
    - transformer: 用于转换显示的输入的函数
    - **kwargs: 额外的参数
    
    #### 示例:
    ```python
    from inquirer_console import Input

    name = Input(message="你的名字是?").prompt()
    print(f"你好, {name}!")
    ```
    """

    def __init__(
            self,
            message: str,
            default: Optional[str] = None,
            validate: Optional[Callable[[str], Union[bool, str]]] = None,
            filter: Optional[Callable[[str], str]] = None,
            transformer: Optional[Callable[[str], str]] = None,
            **kwargs
    ):
        """
        初始化输入提示。
        """
        super().__init__(message, default=default, **kwargs)
        self.validate = validate
        self.filter = filter
        self.transformer = transformer

    def _prompt(self) -> str | None:
        """
        执行提示并返回用户的输入。
        
        Returns:
            用户的输入，或者默认值
        """
        while True:
            # 显示提示消息
            default_display = f" ({self.default})" if self.default is not None else ""
            sys.stdout.write(f"{self.message}{default_display}: ")
            sys.stdout.flush()

            # 获取用户输入
            user_input = input()

            # 如果用户没有输入且有默认值，使用默认值
            if not user_input and self.default is not None:
                user_input = self.default

            # 应用过滤器
            if self.filter:
                try:
                    user_input = self.filter(user_input)
                except Exception as e:
                    sys.stdout.write(f"错误: {str(e)}\n")
                    continue

            # 验证输入
            if self.validate:
                try:
                    validate_result = self.validate(user_input)
                    if validate_result is not True:
                        if isinstance(validate_result, str):
                            sys.stdout.write(f"{validate_result}\n")
                        else:
                            sys.stdout.write("输入无效，请重试。\n")
                        continue
                except Exception as e:
                    sys.stdout.write(f"验证错误: {str(e)}\n")
                    continue

            return user_input
