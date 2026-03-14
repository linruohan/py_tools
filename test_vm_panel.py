#!/usr/bin/env python3
"""测试 VmPanel 的 Tab 切换功能"""

import customtkinter as ctk
from panels.vm_panel import VmPanel

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
