#!/usr/bin/env python3
"""测试 VmPanel 的 Tab 切换功能"""

import os
import sys

sys.path.insert(0, 'D:\\codehub\\py_tools')


# 检查是否在无显示器的 headless 环境中
def is_headless():
    """检测是否在无显示器的 headless 环境中运行."""
    ci_envs = ['CI', 'GITHUB_ACTIONS', 'GITLAB_CI', 'JENKINS_URL', 'BUILD_NUMBER']
    if any(os.environ.get(var) for var in ci_envs):
        return True
    if os.name == 'nt' and os.environ.get('MSYSTEM'):
        return True
    return False


# 在 headless 环境中跳过
if is_headless():
    import pytest

    pytest.skip("CI 环境无图形显示器", allow_module_level=True)

import customtkinter as ctk  # noqa: E402

from panels.vm_panel import VmPanel  # noqa: E402


class TestApp(ctk.CTk):
    """测试应用程序"""

    def __init__(self):
        super().__init__()
        self.title('测试 VmPanel')
        self.geometry('1200x900')

        # 创建 VmPanel
        self.vm_panel = VmPanel(self)
        self.vm_panel.grid(row=0, column=0, sticky='nsew')

        # 配置网格
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


if __name__ == '__main__':
    app = TestApp()
    app.mainloop()
