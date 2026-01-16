import tkinter as tk
from tkinter import END, Listbox


class DragSortListbox(Listbox):
    """支持拖动排序的Listbox子类（黑色背景）"""

    def __init__(self, master, **kwargs):
        # 预设黑色背景相关样式，优先级低于传入的kwargs
        default_kwargs = {
            "bg": "#1a1a1a",  # 深黑色背景（匹配ctk dark主题）
            "fg": "#ffffff",  # 白色文字
            "selectbackground": "#3a3a3a",  # 选中项背景色（浅灰）
            "selectforeground": "#ffffff",  # 选中项文字色
            "activestyle": "none",  # 取消选中时的虚线框
            "bd": 0,  # 去掉边框
            "highlightthickness": 0,  # 去掉聚焦边框
        }
        # 合并默认样式和传入的参数（传入的参数会覆盖默认值）
        default_kwargs.update(kwargs)

        super().__init__(master, **default_kwargs)

        self.drag_index = None  # 记录拖动项的初始索引

        # 绑定拖动事件
        self.bind("<Button-1>", self._on_click)
        self.bind("<B1-Motion>", self._on_drag)

    def _on_click(self, event):
        """鼠标点击时记录选中项索引"""
        self.drag_index = self.nearest(event.y)

    def _on_drag(self, event):
        """鼠标拖动时调整选中项位置"""
        if self.drag_index is None:
            return
        current_index = self.nearest(event.y)
        if current_index != self.drag_index:
            # 获取拖动项的内容
            drag_item = self.get(self.drag_index)
            # 删除原位置项
            self.delete(self.drag_index)
            # 插入到新位置
            self.insert(current_index, drag_item)
            # 更新拖动索引
            self.drag_index = current_index
            # 保持选中状态
            self.selection_set(current_index)


# 测试代码（可直接运行验证效果）
if __name__ == "__main__":
    root = tk.Tk()
    root.title("黑色背景拖动排序Listbox测试")
    root.configure(bg="#1a1a1a")  # 窗口背景也设为黑色
    root.geometry("300x400")

    # 创建自定义Listbox
    listbox = DragSortListbox(
        root,
        font=("Consolas", 12),  # 自定义字体
        height=20,
    )
    listbox.pack(fill="both", expand=True, padx=20, pady=20)

    # 添加测试数据
    test_data = ["Key1", "Key2 [LIST]", "Key3", "Key4 [LIST]", "Key5"]
    for item in test_data:
        listbox.insert(END, item)

    root.mainloop()
