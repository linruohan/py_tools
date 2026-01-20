"""Home Panel"""

import customtkinter as ctk


class HomePanel(ctk.CTkFrame):
    """Home Panel."""

    def __init__(self, parent: ctk.CTk) -> None:
        """初始化Home Panel."""
        super().__init__(parent)
        self.corner_radius = 10
        self.fg_color = "transparent"

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.init_ui()

    def init_ui(self) -> None:
        """初始化UI."""
        self.tabview = ctk.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=0, sticky="nsew")
        # 配置tabview的选项卡高度为紧凑模式
        # 配置选项卡的样式
        self.tabview.configure(
            segmented_button_selected_color=("#3B8ED0", "#1F6AA5"),
            segmented_button_selected_hover_color=("#36719F", "#144870"),
            segmented_button_unselected_color=("#DCE4EE", "#2B2B2B"),
            segmented_button_unselected_hover_color=("#CED8E6", "#3C3C3C"),
            text_color=("gray10", "#DCE4EE"),
            text_color_disabled=("gray60", "gray40"),
        )
        for tab_name in ["CTkTabview", "Tab 2", "Tab 3", "Tab 4", "Tab 5", "Tab 6", "Tab 7", "Tab 8"]:
            self.tabview.add(tab_name)
        self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)
        self.tabview_1()
        self.tabview_2()

    def tabview_1(self) -> None:
        """初始化tab1."""
        self.optionmenu_1 = ctk.CTkOptionMenu(
            self.tabview.tab("CTkTabview"),
            dynamic_resizing=False,
            values=["Value 1", "Value 2", "Value Long Long Long"],
        )
        self.optionmenu_1.grid(row=0, column=0, sticky="w")
        self.combobox_1 = ctk.CTkComboBox(
            self.tabview.tab("CTkTabview"), values=["Value 1", "Value 2", "Value Long....."]
        )
        self.combobox_1.grid(row=1, column=0, sticky="w")
        self.string_input_button = ctk.CTkButton(
            self.tabview.tab("CTkTabview"), text="Open CTkInputDialog", command=self.open_input_dialog_event
        )

    def tabview_2(self) -> None:
        """初始化tab2."""
        self.string_input_button.grid(row=2, column=0, sticky="w")
        self.label_tab_2 = ctk.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, sticky="w")

    def open_input_dialog_event(self) -> None:
        """打开输入对话框."""
        x = self.winfo_x()
        y = self.winfo_y()
        width = self.winfo_width()
        height = self.winfo_height()
        # 在主窗口右侧打开对话框
        dialog_x = x + width + 20
        dialog_y = y + height
        dialog = ctk.CTkInputDialog(text="请输入:", title="旁边对话框")

        # 多次尝试确保位置设置成功
        def set_pos():
            dialog.geometry(f"+{dialog_x}+{dialog_y}")

        dialog.after(10, set_pos)

        result = dialog.get_input()
        print(f"输入结果: {result}")
