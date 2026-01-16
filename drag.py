import tkinter as tk

import customtkinter as ctk

# 设置外观
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class DraggableWidgetApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("拖拽控件到另一个容器")
        self.geometry("800x500")

        # 拖拽相关变量
        self.dragged_widget = None  # 当前被拖拽的控件
        self.start_x = 0  # 鼠标相对于控件的x偏移
        self.start_y = 0  # 鼠标相对于控件的y偏移
        self.start_container = None  # 起始容器
        self.widget_text = ""  # 被拖拽控件的文本
        self.is_dragging = False  # 拖拽状态标记（屏蔽hover事件）

        # 创建主布局
        self._create_main_layout()

    def _create_main_layout(self):
        """创建主界面布局：左侧源容器，右侧目标容器"""
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 左侧源容器
        self.source_frame = ctk.CTkFrame(main_frame, width=350, height=400, fg_color="#f0f0f0")
        self.source_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(self.source_frame, text="源容器（可拖拽控件到右侧）", text_color="#333").pack(pady=10)

        # 右侧目标容器
        self.target_frame = ctk.CTkFrame(main_frame, width=350, height=400, fg_color="#e8e8e8")
        self.target_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(self.target_frame, text="目标容器（接收拖拽的控件）", text_color="#333").pack(pady=10)

        # 创建可拖拽控件
        self._create_draggable_widgets()

    def _create_draggable_widgets(self):
        """创建可拖拽按钮（带防hover报错的自定义按钮）"""
        # 可拖拽按钮1
        self._create_safe_draggable_btn("可拖拽按钮1", self.source_frame)
        # 可拖拽按钮2
        self._create_safe_draggable_btn("可拖拽按钮2", self.source_frame)

    def _create_safe_draggable_btn(self, text, parent):
        """创建安全的可拖拽按钮（屏蔽销毁后的hover事件）"""

        # 创建自定义按钮，重写hover事件避免报错
        class SafeCTkButton(ctk.CTkButton):
            def __init__(self, master, text, app_ref):
                super().__init__(master, text=text, width=200, height=50)
                self.app_ref = app_ref  # 引用主应用，判断拖拽状态
                self.is_destroyed = False  # 标记是否已销毁

            def _on_enter(self, event=None):
                """重写hover进入事件：仅在非拖拽/未销毁时执行"""
                if not self.app_ref.is_dragging and not self.is_destroyed:
                    try:
                        super()._on_enter(event)
                    except tk.TclError:
                        pass

            def _on_leave(self, event=None):
                """重写hover离开事件：仅在非拖拽/未销毁时执行"""
                if not self.app_ref.is_dragging and not self.is_destroyed:
                    try:
                        super()._on_leave(event)
                    except tk.TclError:
                        pass

            def destroy(self):
                """重写销毁方法：标记状态，避免后续事件报错"""
                self.is_destroyed = True
                # 先解除所有事件绑定
                self.unbind("<Enter>")
                self.unbind("<Leave>")
                self.unbind("<Button-1>")
                self.unbind("<B1-Motion>")
                self.unbind("<ButtonRelease-1>")
                # 延迟销毁（避免事件队列残留）
                self.after(10, super().destroy)

        # 创建安全按钮并绑定拖拽事件
        btn = SafeCTkButton(parent, text, self)
        btn.pack(pady=10)

        # 绑定拖拽事件
        btn.bind("<Button-1>", self._on_drag_start)
        btn.bind("<B1-Motion>", self._on_drag_motion)
        btn.bind("<ButtonRelease-1>", self._on_drag_end)

    def _on_drag_start(self, event):
        """拖拽开始：标记状态，记录初始信息"""
        self.is_dragging = True  # 标记拖拽中，屏蔽hover事件
        self.dragged_widget = event.widget
        self.start_x = event.x
        self.start_y = event.y
        self.start_container = self.dragged_widget.master
        self.widget_text = self.dragged_widget.cget("text")

        # 提升控件层级
        self.dragged_widget.tk.call("raise", self.dragged_widget._w)

    def _on_drag_motion(self, event):
        """拖拽过程：平滑移动控件"""
        if not self.dragged_widget or not self.is_dragging:
            return

        # 计算新位置（绝对坐标）
        x = self.dragged_widget.winfo_pointerx() - self.start_x
        y = self.dragged_widget.winfo_pointery() - self.start_y
        # 转换为相对父容器坐标
        x -= self.dragged_widget.master.winfo_rootx()
        y -= self.dragged_widget.master.winfo_rooty()

        # 移动控件
        self.dragged_widget.pack_forget()
        self.dragged_widget.place(x=x, y=y)

    def _on_drag_end(self, event):
        """拖拽结束：判断位置，重建控件"""
        if not self.dragged_widget:
            self.is_dragging = False
            return

        # 1. 获取鼠标落点
        mouse_x = event.x_root
        mouse_y = event.y_root

        # 2. 判断是否在目标容器内
        target_x1 = self.target_frame.winfo_rootx()
        target_y1 = self.target_frame.winfo_rooty()
        target_x2 = target_x1 + self.target_frame.winfo_width()
        target_y2 = target_y1 + self.target_frame.winfo_height()
        in_target = (target_x1 < mouse_x < target_x2) and (target_y1 < mouse_y < target_y2)

        # 3. 销毁原控件（安全销毁）
        self.dragged_widget.destroy()

        # 4. 重建控件到目标容器
        if in_target:
            self._create_safe_draggable_btn(self.widget_text, self.target_frame)
        else:
            self._create_safe_draggable_btn(self.widget_text, self.start_container)

        # 5. 重置拖拽状态
        self.is_dragging = False
        self.dragged_widget = None
        self.start_x = 0
        self.start_y = 0
        self.start_container = None
        self.widget_text = ""


if __name__ == "__main__":
    app = DraggableWidgetApp()
    app.mainloop()
