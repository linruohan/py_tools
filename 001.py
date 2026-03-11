import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("动态标签页示例")
        self.geometry("400x300")

        # 创建标签页控件
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # 添加主标签页
        self.main_tab = self.tabview.add("主标签页")

        # 创建一个开关，绑定变量和事件
        self.toggle_var = ctk.BooleanVar(value=False)
        self.toggle_switch = ctk.CTkSwitch(
            self.main_tab,
            text="显示动态标签页",
            variable=self.toggle_var,
            command=self.toggle_tab
        )
        self.toggle_switch.pack(pady=20)

        # 动态标签页的名称
        self.dynamic_tab_name = "动态页"

    def toggle_tab(self):
        """根据开关状态添加或删除动态标签页"""
        if self.toggle_var.get():
            # 开关打开：尝试添加动态标签页（如果尚未存在）
            try:
                # 检查标签页是否存在（通过尝试获取它）
                self.tabview.tab(self.dynamic_tab_name)
            except ValueError:
                # 不存在，则添加
                self.tabview.add(self.dynamic_tab_name)
                # 在新标签页中放入一些内容
                label = ctk.CTkLabel(
                    self.tabview.tab(self.dynamic_tab_name),
                    text="这是动态添加的标签页"
                )
                label.pack(pady=20)
        else:
            # 开关关闭：尝试删除动态标签页（如果存在）
            try:
                self.tabview.delete(self.dynamic_tab_name)
            except ValueError:
                # 标签页不存在，无需处理
                pass

if __name__ == "__main__":
    app = App()
    app.mainloop()