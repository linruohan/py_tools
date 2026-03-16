"""搜索筛选组件示例."""

import customtkinter as ctk
from components.search_filter import SearchFilter


class SearchFilterExample(ctk.CTk):
    """搜索筛选组件示例应用."""

    def __init__(self):
        super().__init__()
        self.title('搜索筛选组件示例')
        # self.geometry('500x400')
        self.configure(fg_color='#242424')

        # 创建示例数据
        self.sample_items = [
            'Apple', 'Banana', 'Cherry', 'Date', 'Elderberry',
            'Fig', 'Grape', 'Honeydew', 'Kiwi', 'Lemon',
            'Mango', 'Orange', 'Pear', 'Quince', 'Raspberry',
            'Strawberry', 'Tangerine', 'Watermelon'
        ]

        self._init_ui()

    def _init_ui(self):
        """初始化界面."""
        # 创建主框架
        main_frame = ctk.CTkFrame(self, fg_color='transparent')
        main_frame.pack(fill='both', expand=True, padx=0, pady=0)

        # 创建搜索筛选组件
        self.search_filter = SearchFilter(
            main_frame,
            items=self.sample_items,
            on_select_callback=self._on_item_selected,
            placeholder_text='请输入水果名称...',
        )
        self.search_filter.pack(fill='x', pady=0)

        # 创建选中结果显示
        self.result_label = ctk.CTkLabel(
            main_frame,
            text='选中的项目: 无',
            font=('Microsoft YaHei UI', 12)
        )
        self.result_label.pack(pady=0)

        # 创建按钮框架
        button_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        button_frame.pack(pady=10)

    def _on_item_selected(self, item):
        """选中项回调."""
        self.result_label.configure(text=f'选中的项目: {item}')



if __name__ == '__main__':
    app = SearchFilterExample()
    app.mainloop()