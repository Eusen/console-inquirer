"""
跨平台的键盘输入处理模块。
"""
import sys
import os

# 检查当前操作系统
IS_WINDOWS = os.name == 'nt'

if IS_WINDOWS:
    import msvcrt


    def get_key() -> str:
        """
        获取用户按下的按键。Windows实现。
        
        Returns:
            用户按下的按键的字符表示
        """
        if msvcrt.kbhit():
            key = msvcrt.getch()
            # 处理特殊键（如方向键）
            if key == b'\xe0':  # 特殊键前缀
                key = msvcrt.getch()
                if key == b'H':  # 上箭头
                    return 'UP'
                elif key == b'P':  # 下箭头
                    return 'DOWN'
                elif key == b'M':  # 右箭头
                    return 'RIGHT'
                elif key == b'K':  # 左箭头
                    return 'LEFT'
                return key.decode('utf-8')
            # 处理Enter键
            elif key == b'\r':
                return '\r'
            # 处理其他键
            return key.decode('utf-8', errors='replace')
        return ''


    def wait_for_key() -> str:
        """
        等待用户按下一个键。Windows实现。
        
        Returns:
            用户按下的按键的字符表示
        """
        key = msvcrt.getch()
        # 处理特殊键（如方向键）
        if key == b'\xe0':
            key = msvcrt.getch()
            if key == b'H':
                return 'UP'
            elif key == b'P':
                return 'DOWN'
            elif key == b'M':
                return 'RIGHT'
            elif key == b'K':
                return 'LEFT'
            return key.decode('utf-8')
        # 处理Enter键
        elif key == b'\r':
            return '\r'
        # 处理其他键
        return key.decode('utf-8', errors='replace')

else:
    import tty
    import select


    def get_key() -> str:
        """
        获取用户按下的按键。Unix实现。
        
        Returns:
            用户按下的按键的字符表示
        """
        fd = sys.stdin.fileno()

        tty.setraw(fd)
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
            if key == '\x1b':  # 处理特殊键（方向键等）
                seq = sys.stdin.read(2)
                if seq[0] == '[':
                    if seq[1] == 'A':
                        return 'UP'
                    elif seq[1] == 'B':
                        return 'DOWN'
                    elif seq[1] == 'C':
                        return 'RIGHT'
                    elif seq[1] == 'D':
                        return 'LEFT'
            return key
        return ''


    def wait_for_key() -> str:
        """
        等待用户按下一个键。Unix实现。
        
        Returns:
            用户按下的按键的字符表示
        """
        fd = sys.stdin.fileno()
        tty.setraw(fd)
        key = sys.stdin.read(1)
        if key == '\x1b':  # 处理特殊键（方向键等）
            seq = sys.stdin.read(2)
            if seq[0] == '[':
                if seq[1] == 'A':
                    return 'UP'
                elif seq[1] == 'B':
                    return 'DOWN'
                elif seq[1] == 'C':
                    return 'RIGHT'
                elif seq[1] == 'D':
                    return 'LEFT'
        return key
