"""
多行文本输入提示模块，用于获取用户的多行文本输入。
"""
import sys
from typing import Optional, Union, Callable

from ..prompt import BasePrompt


class Text(BasePrompt[str]):
    """
    多行文本输入提示类，用于获取用户的多行文本输入。

    #### Args:
    - message: 向用户显示的提示消息
    - end_text: 结束输入的标记文本，如果设置，用户可以通过输入此文本单独一行结束输入
    - help_text: 帮助文本，向用户解释如何结束输入
    - default: 当用户未输入时的默认值
    - validate: 用于验证用户输入的函数，返回布尔值或错误消息
    - filter: 用于过滤/转换用户输入的函数
    - **kwargs: 额外的参数
    
    #### 示例:
    ```python
    from inquirer_console import Text

    description = Text(
        message="请输入项目描述"
    ).prompt()

    print(f"项目描述:\n{description}")
    ```
    """

    def __init__(
            self,
            message: str,
            end_text: Optional[str] = None,
            help_text: Optional[str] = None,
            default: Optional[str] = None,
            validate: Optional[Callable[[str], Union[bool, str]]] = None,
            filter: Optional[Callable[[str], str]] = None,
            **kwargs
    ):
        """
        初始化多行文本输入提示。
        """
        super().__init__(message, default=default, **kwargs)
        self.end_text = end_text

        # 默认帮助文本
        if help_text is None:
            if end_text:
                self.help_text = f"(连续两次按Enter结束输入，或输入{end_text}单独一行结束输入，Ctrl+C取消)"
            else:
                self.help_text = "(连续两次按Enter结束输入，Ctrl+C取消)"
        else:
            self.help_text = help_text

        self.validate = validate
        self.filter = filter

    def _prompt(self) -> str:
        """
        执行提示并返回用户的多行文本输入。
        
        Returns:
            用户的多行文本输入，或者默认值
        """
        # 显示提示消息和帮助文本
        sys.stdout.write(f"{self.message}\n")
        sys.stdout.write(f"{self.help_text}\n")
        sys.stdout.flush()

        try:
            # 如果有默认值，显示默认值
            if self.default is not None:
                sys.stdout.write(f"默认值:\n{self.default}\n")
                sys.stdout.write(f"按Enter使用默认值，或开始输入覆盖默认值:\n")
                sys.stdout.flush()

                # 检查用户是否直接按了Enter
                first_line = input()
                if not first_line:
                    return self.default

                # 如果用户输入了内容，将其作为第一行
                lines = [first_line]
                empty_line_count = 0
            else:
                lines = []
                empty_line_count = 0

            # 循环接收用户输入
            while True:
                try:
                    line = input()

                    # 检查是否是空行
                    if not line:
                        empty_line_count += 1
                        # 如果连续输入了两个空行，结束输入
                        if empty_line_count >= 2:
                            # 移除最后一个空行（保留一个空行）
                            if lines and not lines[-1]:
                                lines.pop()
                            break
                    else:
                        empty_line_count = 0

                    # 如果设置了end_text，检查是否是结束标记
                    if self.end_text and line == self.end_text:
                        break

                    # 添加到行列表
                    lines.append(line)
                except EOFError:
                    # 捕获输入流结束异常
                    break

            # 将行列表合并为文本
            text = "\n".join(lines)

            # 如果用户没有输入且有默认值，使用默认值
            if not text and self.default is not None:
                text = self.default

            # 应用过滤器
            if self.filter:
                try:
                    text = self.filter(text)
                except Exception as e:
                    sys.stdout.write(f"错误: {str(e)}\n")
                    sys.stdout.flush()
                    return self._prompt()  # 重新开始

            # 验证输入
            if self.validate:
                try:
                    validate_result = self.validate(text)
                    if validate_result is not True:
                        if isinstance(validate_result, str):
                            sys.stdout.write(f"{validate_result}\n")
                        else:
                            sys.stdout.write("输入无效，请重试。\n")
                        sys.stdout.flush()
                        return self._prompt()  # 重新开始
                except Exception as e:
                    sys.stdout.write(f"验证错误: {str(e)}\n")
                    sys.stdout.flush()
                    return self._prompt()  # 重新开始

            return text
        except Exception as e:
            # 处理其他异常
            sys.stdout.write(f"发生错误: {str(e)}\n")
            sys.stdout.flush()
            return self._prompt()  # 重新开始
