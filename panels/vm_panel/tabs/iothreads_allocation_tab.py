"""IO 线程分配配置 Tab - IOThreads Allocation.

根据 libvirt 文档第 24 章实现:
https://www.libvirt.org/formatdomain.html#iothreads-allocation

IOThreads 是专用事件循环线程，用于支持磁盘设备的块 I/O 请求，
可提高 SMP 主机/客户机的可扩展性。
"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class IOThreadsAllocationTab(BaseConfigTab):
    """IO 线程分配配置 Tab."""

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)
        # IOThread ID 列表
        self.iothread_entries = []

    def _init_ui(self) -> None:
        """初始化 UI - 所有 section 合并为一个，每行 pack 布局，左对齐."""
        # 主容器
        main_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=6)
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # 标题
        ctk.CTkLabel(main_frame, text='IO 线程分配', font=CTK_FONT_BOLD, text_color='#64b5f6').pack(
            anchor='w', padx=10, pady=(10, 5)
        )

        # ===== IO 线程数配置行 =====
        iothreads_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        iothreads_frame.pack(fill='x', padx=10, pady=3)

        ctk.CTkLabel(
            iothreads_frame, text='IO 线程数:', font=CTK_FONT_BOLD, width=80, anchor='w'
        ).pack(side='left')

        self.iothreads_var = ctk.StringVar(value='None')
        self.iothreads_menu = ctk.CTkOptionMenu(
            iothreads_frame,
            values=['None', '1', '2', '3', '4', '6', '8', '12', '16'],
            width=70,
            variable=self.iothreads_var,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.iothreads_menu.pack(side='left', padx=5)

        ctk.CTkLabel(
            iothreads_frame,
            text='(建议：每个 IOThread 对应 1-2 个主机 CPU)',
            font=CTK_FONT_SMALL,
            text_color='#888888',
        ).pack(side='left', padx=5)

        # ===== IOThread IDs 配置行 =====
        iothreadids_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        iothreadids_frame.pack(fill='x', padx=10, pady=3)

        ctk.CTkLabel(
            iothreadids_frame, text='IOThread IDs:', font=CTK_FONT_BOLD, width=80, anchor='w'
        ).pack(side='left')

        # 添加按钮
        add_btn = ctk.CTkButton(
            iothreadids_frame,
            text='+ 添加',
            width=60,
            font=CTK_FONT_SMALL,
            command=self._add_iothread_entry,
        )
        add_btn.pack(side='left', padx=(0, 10))

        # IOThread IDs 列表容器
        self.iothread_list_frame = ctk.CTkFrame(iothreadids_frame, fg_color='transparent')
        self.iothread_list_frame.pack(side='left', fill='x', expand=True)
        self.iothread_list_frame.pack_propagate(False)
        self.iothread_list_frame.configure(height=40)

        # 初始不添加条目，由用户手动添加

        # ===== DefaultIOThread 配置行 =====
        defaultiothread_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        defaultiothread_frame.pack(fill='x', padx=10, pady=3)

        ctk.CTkLabel(
            defaultiothread_frame, text='DefaultIOThread:', font=CTK_FONT_BOLD, width=80, anchor='w'
        ).pack(side='left')

        # 线程池最小值
        ctk.CTkLabel(
            defaultiothread_frame, text='线程池最小:', font=CTK_FONT_MAIN, width=70, anchor='w'
        ).pack(side='left', padx=(10, 0))
        self.thread_pool_min = ctk.CTkEntry(defaultiothread_frame, placeholder_text='0', width=60)
        self.thread_pool_min.pack(side='left', padx=(0, 5))
        self.thread_pool_min.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 线程池最大值
        ctk.CTkLabel(
            defaultiothread_frame, text='线程池最大:', font=CTK_FONT_MAIN, width=70, anchor='w'
        ).pack(side='left', padx=(10, 0))
        self.thread_pool_max = ctk.CTkEntry(defaultiothread_frame, placeholder_text='16', width=60)
        self.thread_pool_max.pack(side='left', padx=(0, 5))
        self.thread_pool_max.bind('<KeyRelease>', lambda e: self._trigger_change())

        ctk.CTkLabel(
            defaultiothread_frame,
            text='(默认事件 loop 的 worker 线程边界)',
            font=CTK_FONT_SMALL,
            text_color='#888888',
        ).pack(side='left', padx=5)

        # 说明区域
        info_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        info_frame.pack(fill='x', padx=10, pady=(15, 5))

        info_text = (
            '说明：选择 "None" 或不填值将不生成对应的 XML 元素\n'
            'IO 线程数：定义分配给 domain 的 IOThread 总数，默认从 1 开始顺序编号\n'
            'IOThread IDs：可自定义 IOThread ID，支持设置线程池边界和轮询间隔\n'
            'DefaultIOThread：设置默认事件 loop 的 worker 线程最小/最大边界\n'
            '注意：仅 QEMU/KVM 支持 (libvirt 1.2.8+)'
        )
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=CTK_FONT_SMALL,
            text_color='#888888',
            justify='left',
        ).pack(anchor='w')

    def _add_iothread_entry(self):
        """添加一个 IOThread ID 配置条目."""
        entry_frame = ctk.CTkFrame(self.iothread_list_frame, fg_color='transparent')
        entry_frame.pack(side='left', padx=2, pady=2)

        # ID
        id_entry = ctk.CTkEntry(entry_frame, placeholder_text='ID', width=40)
        id_entry.pack(side='left')
        id_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 线程池最小
        min_entry = ctk.CTkEntry(entry_frame, placeholder_text='min', width=40)
        min_entry.pack(side='left', padx=2)
        min_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 线程池最大
        max_entry = ctk.CTkEntry(entry_frame, placeholder_text='max', width=40)
        max_entry.pack(side='left', padx=2)
        max_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 轮询 max (纳秒)
        poll_max_entry = ctk.CTkEntry(entry_frame, placeholder_text='poll max(ns)', width=90)
        poll_max_entry.pack(side='left', padx=2)
        poll_max_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 轮询 grow
        poll_grow_entry = ctk.CTkEntry(entry_frame, placeholder_text='grow', width=50)
        poll_grow_entry.pack(side='left', padx=2)
        poll_grow_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 轮询 shrink
        poll_shrink_entry = ctk.CTkEntry(entry_frame, placeholder_text='shrink', width=50)
        poll_shrink_entry.pack(side='left', padx=2)
        poll_shrink_entry.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 删除按钮
        del_btn = ctk.CTkButton(
            entry_frame,
            text='X',
            width=30,
            font=CTK_FONT_SMALL,
            command=lambda: self._remove_iothread_entry(entry_frame),
        )
        del_btn.pack(side='left', padx=2)

        self.iothread_entries.append(
            {
                'frame': entry_frame,
                'id': id_entry,
                'thread_pool_min': min_entry,
                'thread_pool_max': max_entry,
                'poll_max': poll_max_entry,
                'poll_grow': poll_grow_entry,
                'poll_shrink': poll_shrink_entry,
            }
        )

        # 更新删除按钮状态
        self._update_delete_buttons()
        self._trigger_change()

    def _remove_iothread_entry(self, entry_frame):
        """删除一个 IOThread ID 配置条目."""
        for i, entry in enumerate(self.iothread_entries):
            if entry['frame'] == entry_frame:
                entry['frame'].destroy()
                self.iothread_entries.pop(i)
                break

        self._update_delete_buttons()
        self._trigger_change()

    def _update_delete_buttons(self):
        """更新删除按钮的可见性."""
        for entry in self.iothread_entries:
            for widget in entry['frame'].winfo_children():
                if isinstance(widget, ctk.CTkButton):
                    if len(self.iothread_entries) == 1:
                        widget.configure(state='disabled')
                    else:
                        widget.configure(state='normal')

    def get_config(self) -> dict:
        """获取配置数据."""
        # 处理 IO 线程数
        iothreads_val = self.iothreads_var.get()
        iothreads = None if iothreads_val == 'None' else int(iothreads_val)

        # 处理 IOThread IDs
        iothreadids = []
        for entry in self.iothread_entries:
            iothread_id = entry['id'].get().strip()
            if not iothread_id:
                continue

            iothread_info = {'id': int(iothread_id)}

            thread_pool_min = entry['thread_pool_min'].get().strip()
            if thread_pool_min:
                iothread_info['thread_pool_min'] = int(thread_pool_min)

            thread_pool_max = entry['thread_pool_max'].get().strip()
            if thread_pool_max:
                iothread_info['thread_pool_max'] = int(thread_pool_max)

            poll_max = entry['poll_max'].get().strip()
            if poll_max:
                iothread_info['poll_max'] = int(poll_max)

            poll_grow = entry['poll_grow'].get().strip()
            if poll_grow:
                iothread_info['poll_grow'] = int(poll_grow)

            poll_shrink = entry['poll_shrink'].get().strip()
            if poll_shrink:
                iothread_info['poll_shrink'] = int(poll_shrink)

            iothreadids.append(iothread_info)

        # 处理 DefaultIOThread
        thread_pool_min = self.thread_pool_min.get().strip()
        thread_pool_max = self.thread_pool_max.get().strip()

        defaultiothread = {}
        if thread_pool_min:
            defaultiothread['thread_pool_min'] = int(thread_pool_min)
        if thread_pool_max:
            defaultiothread['thread_pool_max'] = int(thread_pool_max)

        return {
            'iothreads': iothreads,
            'iothreadids': iothreadids,
            'defaultiothread': defaultiothread if defaultiothread else None,
        }

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        return {'iothreads_allocation': self.get_config()}

    def load_config(self, config: dict) -> None:
        """加载配置数据."""
        if not config:
            # 重置所有配置
            self.iothreads_var.set('None')
            self.thread_pool_min.delete(0, 'end')
            self.thread_pool_max.delete(0, 'end')
            # 清空 IOThread IDs
            for entry in self.iothread_entries:
                entry['frame'].destroy()
            self.iothread_entries = []
            return

        # 加载 IO 线程数
        iothreads = config.get('iothreads')
        if iothreads:
            self.iothreads_var.set(str(iothreads))
        else:
            self.iothreads_var.set('None')

        # 加载 IOThread IDs
        iothreadids = config.get('iothreadids', [])
        for iothread_info in iothreadids:
            self._add_iothread_entry()
            if self.iothread_entries:
                entry = self.iothread_entries[-1]
                entry['id'].insert(0, str(iothread_info.get('id', '')))
                if iothread_info.get('thread_pool_min'):
                    entry['thread_pool_min'].insert(0, str(iothread_info['thread_pool_min']))
                if iothread_info.get('thread_pool_max'):
                    entry['thread_pool_max'].insert(0, str(iothread_info['thread_pool_max']))
                if iothread_info.get('poll_max'):
                    entry['poll_max'].insert(0, str(iothread_info['poll_max']))
                if iothread_info.get('poll_grow'):
                    entry['poll_grow'].insert(0, str(iothread_info['poll_grow']))
                if iothread_info.get('poll_shrink'):
                    entry['poll_shrink'].insert(0, str(iothread_info['poll_shrink']))

        # 加载 DefaultIOThread
        defaultiothread = config.get('defaultiothread', {})
        if defaultiothread:
            if defaultiothread.get('thread_pool_min'):
                self.thread_pool_min.insert(0, str(defaultiothread['thread_pool_min']))
            if defaultiothread.get('thread_pool_max'):
                self.thread_pool_max.insert(0, str(defaultiothread['thread_pool_max']))
