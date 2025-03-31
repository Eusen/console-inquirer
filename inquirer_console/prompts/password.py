"""
密码输入提示模块，用于安全地输入密码。
"""
import sys
import getpass
from typing import Optional, Union, Callable

from ..prompt import BasePrompt


class Password(BasePrompt[str]):
    """
    密码输入提示类，用于安全地输入密码。

    #### Args:
    - message: 向用户显示的提示消息
    - mask: 用于掩盖输入的字符，设置为None则完全隐藏输入
    - validate: 用于验证用户输入的函数，返回布尔值或错误消息
    - **kwargs: 额外的参数

    #### 示例:
    ```python
    from inquirer_console import Password

    password = Password(
        message="请输入您的密码",
        mask="*"  # 可选，设置为None则完全隐藏输入
    ).prompt()

    print(f"密码长度: {len(password)}")
    ```
    """

    def __init__(
            self,
            message: str,
            mask: Optional[str] = "*",
            validate: Optional[Callable[[str], Union[bool, str]]] = None,
            **kwargs
    ):
        """
        初始化密码输入提示。
        """
        super().__init__(message, **kwargs)
        self.mask = mask
        self.validate = validate

    def _prompt(self) -> str:
        """
        执行提示并返回用户输入的密码。
        
        Returns:
            用户输入的密码
        """
        while True:
            if self.mask is None:
                # 完全隐藏输入
                sys.stdout.write(f"{self.message}: ")
                sys.stdout.flush()
                password = getpass.getpass("")
            else:
                # 使用掩码字符显示输入
                password = ""
                sys.stdout.write(f"{self.message}: ")
                sys.stdout.flush()

                while True:
                    char = getpass.getpass("", stream=None)
                    if char == "":  # Enter键
                        break
                    password += char
                    sys.stdout.write(self.mask)
                    sys.stdout.flush()

                sys.stdout.write("\n")
                sys.stdout.flush()

            # 验证输入
            if self.validate:
                try:
                    validate_result = self.validate(password)
                    if validate_result is not True:
                        if isinstance(validate_result, str):
                            sys.stdout.write(f"{validate_result}\n")
                        else:
                            sys.stdout.write("密码无效，请重试。\n")
                        continue
                except Exception as e:
                    sys.stdout.write(f"验证错误: {str(e)}\n")
                    continue

            return password
