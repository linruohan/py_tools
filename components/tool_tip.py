import tkinter as tk

from tkinter import ttk


class ToolTip:
    """为任何控件添加工具提示的简单类"""

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind('<Enter>', self.show_tip)
        self.widget.bind('<Leave>', self.hide_tip)

    def show_tip(self, event=None):
        """显示工具提示"""
        if self.tip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox('insert')  # 获取控件插入光标的位置
        x += self.widget.winfo_rootx() + 25  # 相对于屏幕左上角偏移
        y += self.widget.winfo_rooty() + 20
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # 去掉窗口边框
        tw.wm_geometry(f'+{x}+{y}')
        label = tk.Label(
            tw,
            text=self.text,
            justify=tk.LEFT,
            background='#ffffe0',
            relief=tk.SOLID,
            borderwidth=1,
        )
        label.pack()

    def hide_tip(self, event=None):
        """隐藏工具提示"""
        if self.tip_window:
            self.tip_window.destroy()
        self.tip_window = None
