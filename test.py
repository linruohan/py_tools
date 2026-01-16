import json
import re
from tkinter import END, MULTIPLE, Listbox, filedialog, messagebox

import customtkinter as ctk
import pandas as pd

# 设置 customtkinter 外观
ctk.set_appearance_mode("dark")  # 可选: "light", "dark", "system"
ctk.set_default_color_theme("blue")

class JSONToExcelTool(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 窗口配置
        self.title("JSON 处理工具 - 转 Excel")
        self.geometry("1000x700")
        self.minsize(800, 600)

        # 全局变量
        self.json_data = None
        self.original_main_keys = []  # 保存原始主Key
        self.current_selected_list_key = None  # 当前选中的列表Key
        self.current_list_data = None  # 当前选中列表的数据
        self.current_list_keys = []  # 当前列表的内部Key

        # 创建UI布局
        self._create_widgets()

    def _create_widgets(self):
        # ========== 顶部JSON输入区域 ==========
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill="x", padx=20, pady=10)

        input_label = ctk.CTkLabel(input_frame, text="JSON 输入:", font=("Arial", 12, "bold"))
        input_label.pack(anchor="w", padx=10, pady=5)

        # JSON输入文本框
        self.json_textbox = ctk.CTkTextbox(input_frame, height=150, font=("Consolas", 10))
        self.json_textbox.pack(fill="both", padx=10, pady=5, expand=True)

        # 功能按钮
        btn_frame = ctk.CTkFrame(input_frame)
        btn_frame.pack(side="right", padx=10, pady=5)

        parse_btn = ctk.CTkButton(btn_frame, text="解析 JSON", command=self.parse_json)
        parse_btn.pack(side="left", padx=5)

        self.back_btn = ctk.CTkButton(btn_frame, text="返回主Key", command=self.back_to_main_keys, state="disabled")
        self.back_btn.pack(side="left", padx=5)

        # ========== 中间Key展示区域 ==========
        middle_frame = ctk.CTkFrame(self)
        middle_frame.pack(fill="both", padx=20, pady=10, expand=True)

        # Key列表区域
        key_frame = ctk.CTkFrame(middle_frame)
        key_frame.pack(fill="both", padx=10, pady=10, expand=True)

        self.key_label = ctk.CTkLabel(key_frame, text="JSON 主Key列表", font=("Arial", 12, "bold"))
        self.key_label.pack(anchor="w", padx=10, pady=5)

        # 排序按钮
        sort_frame = ctk.CTkFrame(key_frame)
        sort_frame.pack(fill="x", padx=10, pady=5)

        sort_asc_btn = ctk.CTkButton(sort_frame, text="升序排序", command=lambda: self.sort_keys("asc"), width=80)
        sort_asc_btn.pack(side="left", padx=5)

        sort_desc_btn = ctk.CTkButton(sort_frame, text="降序排序", command=lambda: self.sort_keys("desc"), width=80)
        sort_desc_btn.pack(side="left", padx=5)

        # Key列表框（支持多选）
        self.key_listbox = Listbox(key_frame, selectmode=MULTIPLE, font=("Consolas", 10))
        self.key_listbox.pack(fill="both", padx=10, pady=5, expand=True)
        self.key_listbox.bind("<<ListboxSelect>>", self.on_key_select)

        # ========== 底部操作区域 ==========
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.pack(fill="x", padx=20, pady=10)

        # 生成Excel按钮
        generate_btn = ctk.CTkButton(bottom_frame, text="生成 Excel 文件", command=self.generate_excel,
                                     font=("Arial", 12, "bold"), height=40)
        generate_btn.pack(padx=10, pady=10)

    def parse_json(self):
        """解析输入的JSON文本"""
        try:
            # 清空列表
            self.key_listbox.delete(0, END)

            # 获取文本框内容
            json_text = self.json_textbox.get("1.0", END).strip()
            if not json_text:
                messagebox.showwarning("警告", "请输入JSON文本！")
                return

            # 解析JSON
            self.json_data = json.loads(json_text)

            # 检查是否为字典类型
            if not isinstance(self.json_data, dict):
                messagebox.showwarning("警告", "JSON根节点必须是对象（字典）类型！")
                return

            # 获取所有原始主Key并显示
            self.original_main_keys = list(self.json_data.keys())
            self.current_selected_list_key = None
            self.current_list_data = None
            self.current_list_keys = []

            # 显示原始主Key（标记列表类型）
            for key in self.original_main_keys:
                value_type = " [LIST]" if isinstance(self.json_data[key], list) else ""
                self.key_listbox.insert(END, f"{key}{value_type}")

            # 更新UI状态
            self.key_label.configure(text="JSON 主Key列表")
            self.back_btn.configure(state="disabled")

            messagebox.showinfo("成功", "JSON解析成功！")

        except json.JSONDecodeError as e:
            messagebox.showerror("错误", f"JSON格式错误：{e!s}")
        except Exception as e:
            messagebox.showerror("错误", f"解析失败：{e!s}")

    def on_key_select(self, event):
        """选中Key后的回调函数"""
        selected_indices = self.key_listbox.curselection()
        if not selected_indices:
            return

        selected_index = selected_indices[0]
        selected_key_display = self.key_listbox.get(selected_index)

        # 如果当前显示的是原始主Key
        if self.current_selected_list_key is None:
            # 清理类型标记，获取纯Key名称
            pure_key = re.sub(r" \[LIST\]$", "", selected_key_display)

            # 检查该Key是否为列表类型
            if pure_key in self.json_data and isinstance(self.json_data[pure_key], list):
                list_data = self.json_data[pure_key]
                # 确保列表非空且第一个元素是字典
                if len(list_data) > 0 and isinstance(list_data[0], dict):
                    self.current_selected_list_key = pure_key
                    self.current_list_data = list_data
                    self.current_list_keys = list(list_data[0].keys())

                    # 清空列表并显示该列表的内部Key
                    self.key_listbox.delete(0, END)
                    for key in self.current_list_keys:
                        self.key_listbox.insert(END, key)

                    # 更新UI
                    self.key_label.configure(text=f"{pure_key} 列表的内部Key")
                    self.back_btn.configure(state="normal")

    def back_to_main_keys(self):
        """返回显示原始主Key列表"""
        # 清空列表
        self.key_listbox.delete(0, END)

        # 重新显示原始主Key
        for key in self.original_main_keys:
            value_type = " [LIST]" if isinstance(self.json_data[key], list) else ""
            self.key_listbox.insert(END, f"{key}{value_type}")

        # 重置状态
        self.key_label.configure(text="JSON 主Key列表")
        self.back_btn.configure(state="disabled")
        self.current_selected_list_key = None
        self.current_list_data = None
        self.current_list_keys = []

    def sort_keys(self, sort_type):
        """对当前显示的Key进行排序"""
        if self.current_selected_list_key:
            # 排序列表内部Key
            if not self.current_list_keys:
                messagebox.showwarning("警告", "暂无Key可排序！")
                return

            if sort_type == "asc":
                self.current_list_keys.sort()
            else:
                self.current_list_keys.sort(reverse=True)

            # 重新显示
            self.key_listbox.delete(0, END)
            for key in self.current_list_keys:
                self.key_listbox.insert(END, key)
        else:
            # 排序原始主Key
            if not self.original_main_keys:
                messagebox.showwarning("警告", "暂无Key可排序！")
                return

            if sort_type == "asc":
                self.original_main_keys.sort()
            else:
                self.original_main_keys.sort(reverse=True)

            # 重新显示
            self.key_listbox.delete(0, END)
            for key in self.original_main_keys:
                value_type = " [LIST]" if isinstance(self.json_data[key], list) else ""
                self.key_listbox.insert(END, f"{key}{value_type}")

    def generate_excel(self):
        """根据选中的Key生成Excel文件"""
        try:
            if not self.json_data:
                messagebox.showwarning("警告", "请先解析有效的JSON数据！")
                return

            # 情况1：选中了列表Key（如authors），显示的是列表内部Key
            if self.current_selected_list_key and self.current_list_data:
                # 获取选中的列表内部Key
                selected_indices = self.key_listbox.curselection()
                if not selected_indices:
                    messagebox.showwarning("警告", "请至少选择一个列表内部Key！")
                    return

                # 收集选中的Key
                selected_keys = [self.current_list_keys[idx] for idx in selected_indices]

                # 提取数据
                excel_data = []
                for item in self.current_list_data:
                    if isinstance(item, dict):
                        row_data = {k: item.get(k, "") for k in selected_keys}
                        excel_data.append(row_data)

                if not excel_data:
                    messagebox.showwarning("警告", "没有可导出的数据！")
                    return

                # 转换为DataFrame
                df = pd.DataFrame(excel_data)

                # 选择保存路径
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")],
                    title="保存Excel文件",
                    initialfile=f"{self.current_selected_list_key}.xlsx",
                )

                if file_path:
                    # 写入Excel文件（工作表名使用选中的列表Key）
                    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
                        # 工作表名称过长会报错，进行截断
                        safe_sheet_name = self.current_selected_list_key[:31]
                        df.to_excel(writer, sheet_name=safe_sheet_name, index=False)

                    messagebox.showinfo("成功", f"Excel文件已生成：{file_path}")

            # 情况2：显示的是原始主Key
            else:
                selected_indices = self.key_listbox.curselection()
                if not selected_indices:
                    messagebox.showwarning("警告", "请先选择一个列表类型的主Key！")
                    return

                messagebox.showinfo("提示", "请先选中一个列表类型的主Key（如authors），进入其内部Key列表后再导出！")

        except Exception as e:
            messagebox.showerror("错误", f"生成Excel失败：{e!s}")

if __name__ == "__main__":
    # 确保安装了必要的依赖
    try:
        import customtkinter
        import openpyxl
        import pandas
    except ImportError:
        print("缺少依赖包，请执行以下命令安装：")
        print("pip install customtkinter pandas openpyxl")
    else:
        app = JSONToExcelTool()
        app.mainloop()
