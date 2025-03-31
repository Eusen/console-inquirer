"""
基础提示模块，提供了所有提示类型的基础类和功能。
"""
import abc
import signal
from typing import Any, Dict, Optional, TypeVar, Generic, List


class ExitPromptError(Exception):
    """当用户强制退出提示时抛出的异常。"""

    def __init__(self, message="用户强制关闭了提示"):
        self.message = message
        super().__init__(self.message)


T = TypeVar('T')


class BasePrompt(Generic[T], abc.ABC):
    """所有提示类型的基类。"""

    def __init__(self, message: str, name: Optional[str] = None,
                 default: Optional[T] = None, **kwargs):
        """
        初始化提示。
        
        Args:
            message: 向用户显示的提示消息
            name: 提示的名称，用于在answers字典中存储答案
            default: 默认值，当用户未输入时使用
            **kwargs: 额外的参数
        """
        self.message = message
        self.name = name
        self.default = default
        self.options = kwargs
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """设置信号处理器以处理Ctrl+C等中断。"""
        # 保存原始的SIGINT处理器
        self._original_sigint = signal.getsignal(signal.SIGINT)

        # 设置新的SIGINT处理器
        def sigint_handler(signum, frame):
            # 恢复原始处理器
            signal.signal(signal.SIGINT, self._original_sigint)
            # 抛出自定义异常
            raise ExitPromptError()

        signal.signal(signal.SIGINT, sigint_handler)

    def _restore_signal_handlers(self):
        """恢复原始信号处理器。"""
        signal.signal(signal.SIGINT, self._original_sigint)

    @abc.abstractmethod
    def _prompt(self) -> T:
        """实际的提示逻辑，由子类实现。"""
        pass

    def prompt(self) -> T:
        """
        执行提示并返回用户的答案。
        
        Returns:
            用户的回答
        
        Raises:
            ExitPromptError: 当用户通过Ctrl+C强制退出提示时
        """
        try:
            answer = self._prompt()
            return answer
        finally:
            self._restore_signal_handlers()


class Inquirer:
    """
    Inquirer主类，用于创建和执行提示。
    
    示例:
        ```python
        from core.inquirer import Inquirer
        
        answers = Inquirer().prompt([
            {
                'type': 'input',
                'name': 'name',
                'message': '你的名字是?'
            },
            {
                'type': 'confirm',
                'name': 'likes_python',
                'message': '你喜欢Python吗?',
                'default': True
            }
        ])
        
        print(f"你好, {answers['name']}!")
        if answers['likes_python']:
            print("太好了，我也喜欢Python!")
        ```
    """

    def __init__(self):
        """初始化Inquirer。"""
        self._prompts = {}

    def register_prompt(self, name: str, prompt_class):
        """
        注册一个新的提示类型。
        
        Args:
            name: 提示类型的名称
            prompt_class: 提示类的引用
        """
        self._prompts[name] = prompt_class

    def prompt(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        执行一系列提示并返回所有答案。
        
        Args:
            questions: 提示配置的列表
        
        Returns:
            包含所有回答的字典，键为每个提示的name
        
        Raises:
            ExitPromptError: 当用户通过Ctrl+C强制退出提示时
        """
        answers = {}

        for question in questions:
            prompt_type = question.pop('type')
            name = question.pop('name')

            if prompt_type not in self._prompts:
                raise ValueError(f"未知的提示类型: {prompt_type}")

            prompt_class = self._prompts[prompt_type]
            prompt = prompt_class(name=name, **question)

            answer = prompt.prompt()
            answers[name] = answer

        return answers


# 全局实例，可直接导入使用
inquirer = Inquirer()
