"""
确认提示模块，用于获取用户的是/否回答。
"""
import sys
from typing import Optional

from ..prompt import BasePrompt


class Confirm(BasePrompt[bool]):
    """
    确认提示类，用于获取用户的是/否回答。

    #### Args:
    - message: 向用户显示的提示消息
    - default: 当用户未输入时的默认值，True表示是，False表示否
    - **kwargs: 额外的参数
    
    #### 示例:
    ```python
    from inquirer_console import Confirm

    likes_python = Confirm(message="你喜欢Python吗?", default=True).prompt()
    if likes_python:
        print("太好了，我也喜欢Python!")
    ```
    """

    def __init__(self, message: str, default: Optional[bool] = True, **kwargs):
        """
        初始化确认提示。
        """
        super().__init__(message, default=default, **kwargs)

    def _prompt(self) -> bool | None:
        """
        执行提示并返回用户的是/否回答。
        
        Returns:
            用户的回答，True表示是，False表示否
        """
        while True:
            # 显示提示消息
            yes_no = "(Y/n)" if self.default else "(y/N)"
            sys.stdout.write(f"{self.message} {yes_no}: ")
            sys.stdout.flush()

            # 获取用户输入
            user_input = input().lower().strip()

            # 如果用户没有输入，使用默认值
            if not user_input:
                return self.default

            # 判断用户输入
            if user_input in ('y', 'yes', '是', '1', 'true'):
                return True
            elif user_input in ('n', 'no', '否', '0', 'false'):
                return False
            else:
                sys.stdout.write("请输入 'y' 或 'n'。\n")
                continue
