"""时间同步配置 Tab - Clock 配置.

根据 libvirt 文档实现:
https://www.libvirt.org/formatdomain.html#time-keeping
"""

import customtkinter as ctk

from components.base_tab import BaseConfigTab
from utils.styles import BG_COLOR_CONTENT, CTK_FONT_BOLD, CTK_FONT_MAIN, CTK_FONT_SMALL


class TimeKeepingTab(BaseConfigTab):
    """时间同步配置 Tab.

    支持以下配置:
    - clock offset: utc, localtime, timezone, variable, absolute
    - rtc timer: tickpolicy, track, catchup 配置
    - pit timer: tickpolicy
    - tsc timer: mode, frequency
    - hpet timer: present
    - kvmclock timer: present
    """

    def __init__(self, master, on_change_callback=None, **kwargs):
        super().__init__(master, on_change_callback, **kwargs)

        self._init_ui()

    def _init_ui(self) -> None:
        """初始化界面 - 使用 pack 布局，每组元素一行."""
        # ========== 左侧面板 - 时钟偏移配置 ==========
        left_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        left_frame.pack(side='left', fill='both', expand=True, padx=8, pady=8)

        # 左侧面板标题
        left_title = ctk.CTkLabel(
            left_frame,
            text='⏰ 时钟偏移配置',
            font=CTK_FONT_BOLD,
            text_color='#64b5f6',
        )
        left_title.pack(anchor='w', padx=12, pady=(12, 8))

        # 偏移模式行
        row_frame = ctk.CTkFrame(left_frame, fg_color='transparent')
        row_frame.pack(anchor='w', padx=12, pady=4)
        ctk.CTkLabel(row_frame, text='偏移模式:', font=CTK_FONT_MAIN, width=80, anchor='w').pack(
            side='left', padx=(0, 8)
        )
        self.offset = ctk.CTkOptionMenu(
            row_frame,
            values=['None', 'utc', 'localtime', 'timezone', 'variable', 'absolute'],
            width=110,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.offset.set('None')
        self.offset.pack(side='left', padx=4)

        # 时区行 (offset=timezone 时使用)
        row_frame = ctk.CTkFrame(left_frame, fg_color='transparent')
        row_frame.pack(anchor='w', padx=12, pady=4)
        ctk.CTkLabel(row_frame, text='时区:', font=CTK_FONT_MAIN, width=80, anchor='w').pack(
            side='left', padx=(0, 8)
        )
        self.timezone = ctk.CTkEntry(
            row_frame, placeholder_text='Asia/Shanghai', width=140, font=CTK_FONT_SMALL
        )
        self.timezone.pack(side='left', padx=4)
        self.timezone.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 时间调整行 (offset=variable 时使用)
        row_frame = ctk.CTkFrame(left_frame, fg_color='transparent')
        row_frame.pack(anchor='w', padx=12, pady=4)
        ctk.CTkLabel(row_frame, text='时间调整:', font=CTK_FONT_MAIN, width=80, anchor='w').pack(
            side='left', padx=(0, 8)
        )
        self.adjustment = ctk.CTkEntry(
            row_frame, placeholder_text='秒数', width=100, font=CTK_FONT_SMALL
        )
        self.adjustment.pack(side='left', padx=4)
        self.adjustment.bind('<KeyRelease>', lambda e: self._trigger_change())
        ctk.CTkLabel(row_frame, text='秒', font=CTK_FONT_SMALL, text_color='#888888').pack(
            side='left', padx=4
        )

        # 基准行 (offset=variable 时使用)
        row_frame = ctk.CTkFrame(left_frame, fg_color='transparent')
        row_frame.pack(anchor='w', padx=12, pady=4)
        ctk.CTkLabel(row_frame, text='基准:', font=CTK_FONT_MAIN, width=80, anchor='w').pack(
            side='left', padx=(0, 8)
        )
        self.basis = ctk.CTkOptionMenu(
            row_frame,
            values=['None', 'utc', 'localtime'],
            width=100,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.basis.set('None')
        self.basis.pack(side='left', padx=4)

        # 起始时间行 (offset=absolute 时使用)
        row_frame = ctk.CTkFrame(left_frame, fg_color='transparent')
        row_frame.pack(anchor='w', padx=12, pady=4)
        ctk.CTkLabel(row_frame, text='起始时间:', font=CTK_FONT_MAIN, width=80, anchor='w').pack(
            side='left', padx=(0, 8)
        )
        self.start = ctk.CTkEntry(
            row_frame, placeholder_text='Unix 时间戳', width=140, font=CTK_FONT_SMALL
        )
        self.start.pack(side='left', padx=4)
        self.start.bind('<KeyRelease>', lambda e: self._trigger_change())

        # 左侧说明信息
        left_info = ctk.CTkLabel(
            left_frame,
            text='偏移模式说明:\n'
            '• utc: 始终同步到 UTC 时间\n'
            '• localtime: 同步到主机本地时间\n'
            '• timezone: 同步到指定时区\n'
            '• variable: 应用可调整的时间偏移\n'
            '• absolute: 使用固定的时间戳',
            font=CTK_FONT_SMALL,
            text_color='#888888',
            justify='left',
        )
        left_info.pack(anchor='w', padx=12, pady=(8, 12))

        # ========== 右侧面板 - 定时器配置 ==========
        right_frame = ctk.CTkFrame(self, fg_color=BG_COLOR_CONTENT, corner_radius=8)
        right_frame.pack(side='left', fill='both', expand=True, padx=8, pady=8)

        # 右侧面板标题
        right_title = ctk.CTkLabel(
            right_frame,
            text='⏱️ 定时器配置',
            font=CTK_FONT_BOLD,
            text_color='#4caf50',
        )
        right_title.pack(anchor='w', padx=12, pady=(12, 8))

        # RTC Timer 行
        row_frame = ctk.CTkFrame(right_frame, fg_color='transparent')
        row_frame.pack(anchor='w', padx=12, pady=4)
        ctk.CTkLabel(
            row_frame,
            text='RTC 定时器:',
            font=CTK_FONT_BOLD,
            text_color='#4caf50',
            width=90,
            anchor='w',
        ).pack(side='left', padx=(0, 8))
        ctk.CTkLabel(row_frame, text='启用:', font=CTK_FONT_MAIN, width=40, anchor='w').pack(
            side='left', padx=(0, 4)
        )
        self.rtc_present = ctk.CTkOptionMenu(
            row_frame,
            values=['None', 'yes', 'no'],
            width=60,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.rtc_present.set('None')
        self.rtc_present.pack(side='left', padx=4)
        ctk.CTkLabel(row_frame, text='策略:', font=CTK_FONT_MAIN, width=40, anchor='w').pack(
            side='left', padx=(0, 4)
        )
        self.rtc_tickpolicy = ctk.CTkOptionMenu(
            row_frame,
            values=['None', 'catchup', 'delay', 'merge', 'discard'],
            width=90,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.rtc_tickpolicy.set('None')
        self.rtc_tickpolicy.pack(side='left', padx=4)
        ctk.CTkLabel(row_frame, text='跟踪:', font=CTK_FONT_MAIN, width=40, anchor='w').pack(
            side='left', padx=(0, 4)
        )
        self.rtc_track = ctk.CTkOptionMenu(
            row_frame,
            values=['None', 'boot', 'guest', 'wall', 'realtime'],
            width=80,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.rtc_track.set('None')
        self.rtc_track.pack(side='left', padx=4)

        # RTC Catchup 子配置行
        row_frame = ctk.CTkFrame(right_frame, fg_color='transparent')
        row_frame.pack(anchor='w', padx=12, pady=4)
        ctk.CTkLabel(row_frame, text='', font=CTK_FONT_MAIN, width=90, anchor='w').pack(
            side='left', padx=(0, 8)
        )
        ctk.CTkLabel(row_frame, text='Catchup:', font=CTK_FONT_MAIN, width=55, anchor='w').pack(
            side='left', padx=(0, 4)
        )
        self.rtc_catchup_threshold = ctk.CTkEntry(
            row_frame, placeholder_text='阈值', width=50, font=CTK_FONT_SMALL
        )
        self.rtc_catchup_threshold.pack(side='left', padx=2)
        self.rtc_catchup_threshold.bind('<KeyRelease>', lambda e: self._trigger_change())
        self.rtc_catchup_slew = ctk.CTkEntry(
            row_frame, placeholder_text='速率', width=50, font=CTK_FONT_SMALL
        )
        self.rtc_catchup_slew.pack(side='left', padx=2)
        self.rtc_catchup_slew.bind('<KeyRelease>', lambda e: self._trigger_change())
        self.rtc_catchup_limit = ctk.CTkEntry(
            row_frame, placeholder_text='限制', width=50, font=CTK_FONT_SMALL
        )
        self.rtc_catchup_limit.pack(side='left', padx=2)
        self.rtc_catchup_limit.bind('<KeyRelease>', lambda e: self._trigger_change())

        # PIT Timer 行
        row_frame = ctk.CTkFrame(right_frame, fg_color='transparent')
        row_frame.pack(anchor='w', padx=12, pady=4)
        ctk.CTkLabel(
            row_frame,
            text='PIT 定时器:',
            font=CTK_FONT_BOLD,
            text_color='#4caf50',
            width=90,
            anchor='w',
        ).pack(side='left', padx=(0, 8))
        ctk.CTkLabel(row_frame, text='启用:', font=CTK_FONT_MAIN, width=40, anchor='w').pack(
            side='left', padx=(0, 4)
        )
        self.pit_present = ctk.CTkOptionMenu(
            row_frame,
            values=['None', 'yes', 'no'],
            width=60,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.pit_present.set('None')
        self.pit_present.pack(side='left', padx=4)
        ctk.CTkLabel(row_frame, text='策略:', font=CTK_FONT_MAIN, width=40, anchor='w').pack(
            side='left', padx=(0, 4)
        )
        self.pit_tickpolicy = ctk.CTkOptionMenu(
            row_frame,
            values=['None', 'delay', 'catchup', 'merge', 'discard'],
            width=90,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.pit_tickpolicy.set('None')
        self.pit_tickpolicy.pack(side='left', padx=4)

        # TSC Timer 行
        row_frame = ctk.CTkFrame(right_frame, fg_color='transparent')
        row_frame.pack(anchor='w', padx=12, pady=4)
        ctk.CTkLabel(
            row_frame,
            text='TSC 定时器:',
            font=CTK_FONT_BOLD,
            text_color='#4caf50',
            width=90,
            anchor='w',
        ).pack(side='left', padx=(0, 8))
        ctk.CTkLabel(row_frame, text='启用:', font=CTK_FONT_MAIN, width=40, anchor='w').pack(
            side='left', padx=(0, 4)
        )
        self.tsc_present = ctk.CTkOptionMenu(
            row_frame,
            values=['None', 'yes', 'no'],
            width=60,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.tsc_present.set('None')
        self.tsc_present.pack(side='left', padx=4)
        ctk.CTkLabel(row_frame, text='模式:', font=CTK_FONT_MAIN, width=40, anchor='w').pack(
            side='left', padx=(0, 4)
        )
        self.tsc_mode = ctk.CTkOptionMenu(
            row_frame,
            values=['None', 'auto', 'native', 'emulate', 'paravirt', 'smpsafe'],
            width=90,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.tsc_mode.set('None')
        self.tsc_mode.pack(side='left', padx=4)

        # TSC Frequency 行
        row_frame = ctk.CTkFrame(right_frame, fg_color='transparent')
        row_frame.pack(anchor='w', padx=12, pady=4)
        ctk.CTkLabel(row_frame, text='', font=CTK_FONT_MAIN, width=90, anchor='w').pack(
            side='left', padx=(0, 8)
        )
        ctk.CTkLabel(row_frame, text='频率:', font=CTK_FONT_MAIN, width=40, anchor='w').pack(
            side='left', padx=(0, 4)
        )
        self.tsc_frequency = ctk.CTkEntry(
            row_frame, placeholder_text='Hz', width=120, font=CTK_FONT_SMALL
        )
        self.tsc_frequency.pack(side='left', padx=4)
        self.tsc_frequency.bind('<KeyRelease>', lambda e: self._trigger_change())

        # HPET Timer 行
        row_frame = ctk.CTkFrame(right_frame, fg_color='transparent')
        row_frame.pack(anchor='w', padx=12, pady=4)
        ctk.CTkLabel(
            row_frame,
            text='HPET 定时器:',
            font=CTK_FONT_BOLD,
            text_color='#4caf50',
            width=90,
            anchor='w',
        ).pack(side='left', padx=(0, 8))
        ctk.CTkLabel(row_frame, text='启用:', font=CTK_FONT_MAIN, width=40, anchor='w').pack(
            side='left', padx=(0, 4)
        )
        self.hpet_present = ctk.CTkOptionMenu(
            row_frame,
            values=['None', 'yes', 'no'],
            width=60,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.hpet_present.set('None')
        self.hpet_present.pack(side='left', padx=4)

        # KVM Clock 行
        row_frame = ctk.CTkFrame(right_frame, fg_color='transparent')
        row_frame.pack(anchor='w', padx=12, pady=4)
        ctk.CTkLabel(
            row_frame,
            text='KVM Clock:',
            font=CTK_FONT_BOLD,
            text_color='#4caf50',
            width=90,
            anchor='w',
        ).pack(side='left', padx=(0, 8))
        ctk.CTkLabel(row_frame, text='启用:', font=CTK_FONT_MAIN, width=40, anchor='w').pack(
            side='left', padx=(0, 4)
        )
        self.kvmclock_present = ctk.CTkOptionMenu(
            row_frame,
            values=['None', 'yes', 'no'],
            width=60,
            font=CTK_FONT_SMALL,
            command=self._trigger_change,
        )
        self.kvmclock_present.set('None')
        self.kvmclock_present.pack(side='left', padx=4)

        # 右侧说明信息
        right_info = ctk.CTkLabel(
            right_frame,
            text='定时器策略说明:\n'
            '• catchup: 加速补发错过的滴答\n'
            '• delay: 延迟交付，保持正常速率\n'
            '• merge: 合并错过的滴答\n'
            '• discard: 丢弃错过的滴答\n'
            '• None: 不生成此配置',
            font=CTK_FONT_SMALL,
            text_color='#888888',
            justify='left',
        )
        right_info.pack(anchor='w', padx=12, pady=(8, 12))

    def get_config(self) -> dict:
        """获取配置数据."""
        config = {
            'offset': self.offset.get() if self.offset.get() != 'None' else None,
            'timezone': self.timezone.get().strip(),
            'adjustment': self.adjustment.get().strip(),
            'basis': self.basis.get() if self.basis.get() != 'None' else None,
            'start': self.start.get().strip(),
            'timers': {
                'rtc': {
                    'present': self.rtc_present.get() if self.rtc_present.get() != 'None' else None,
                    'tickpolicy': self.rtc_tickpolicy.get()
                    if self.rtc_tickpolicy.get() != 'None'
                    else None,
                    'track': self.rtc_track.get() if self.rtc_track.get() != 'None' else None,
                    'catchup_threshold': self.rtc_catchup_threshold.get().strip(),
                    'catchup_slew': self.rtc_catchup_slew.get().strip(),
                    'catchup_limit': self.rtc_catchup_limit.get().strip(),
                },
                'pit': {
                    'present': self.pit_present.get() if self.pit_present.get() != 'None' else None,
                    'tickpolicy': self.pit_tickpolicy.get()
                    if self.pit_tickpolicy.get() != 'None'
                    else None,
                },
                'tsc': {
                    'present': self.tsc_present.get() if self.tsc_present.get() != 'None' else None,
                    'mode': self.tsc_mode.get() if self.tsc_mode.get() != 'None' else None,
                    'frequency': self.tsc_frequency.get().strip(),
                },
                'hpet': {
                    'present': self.hpet_present.get()
                    if self.hpet_present.get() != 'None'
                    else None,
                },
                'kvmclock': {
                    'present': self.kvmclock_present.get()
                    if self.kvmclock_present.get() != 'None'
                    else None,
                },
            },
        }
        return config

    def to_xml(self) -> dict:
        """生成 XML 配置字典."""
        return {'time_keeping': self.get_config()}

    def load_config(self, config: dict) -> None:
        """加载配置数据.

        Args:
            config: 包含 time_keeping 配置的字典
        """
        if not config:
            self._reset_to_none()
            return

        # 加载 offset 配置
        offset = config.get('offset')
        self.offset.set(offset if offset else 'None')

        # 加载 timezone
        self.timezone.delete(0, 'end')
        timezone = config.get('timezone')
        if timezone:
            self.timezone.insert(0, timezone)

        # 加载 adjustment
        self.adjustment.delete(0, 'end')
        adjustment = config.get('adjustment')
        if adjustment:
            self.adjustment.insert(0, str(adjustment))

        # 加载 basis
        basis = config.get('basis')
        self.basis.set(basis if basis else 'None')

        # 加载 start
        self.start.delete(0, 'end')
        start = config.get('start')
        if start:
            self.start.insert(0, str(start))

        # 加载 timers 配置
        timers = config.get('timers', {})

        # RTC timer
        rtc = timers.get('rtc', {})
        rtc_present = rtc.get('present')
        self.rtc_present.set(rtc_present if rtc_present else 'None')
        rtc_tickpolicy = rtc.get('tickpolicy')
        self.rtc_tickpolicy.set(rtc_tickpolicy if rtc_tickpolicy else 'None')
        rtc_track = rtc.get('track')
        self.rtc_track.set(rtc_track if rtc_track else 'None')

        self.rtc_catchup_threshold.delete(0, 'end')
        threshold = rtc.get('catchup_threshold')
        if threshold:
            self.rtc_catchup_threshold.insert(0, str(threshold))

        self.rtc_catchup_slew.delete(0, 'end')
        slew = rtc.get('catchup_slew')
        if slew:
            self.rtc_catchup_slew.insert(0, str(slew))

        self.rtc_catchup_limit.delete(0, 'end')
        limit = rtc.get('catchup_limit')
        if limit:
            self.rtc_catchup_limit.insert(0, str(limit))

        # PIT timer
        pit = timers.get('pit', {})
        pit_present = pit.get('present')
        self.pit_present.set(pit_present if pit_present else 'None')
        pit_tickpolicy = pit.get('tickpolicy')
        self.pit_tickpolicy.set(pit_tickpolicy if pit_tickpolicy else 'None')

        # TSC timer
        tsc = timers.get('tsc', {})
        tsc_present = tsc.get('present')
        self.tsc_present.set(tsc_present if tsc_present else 'None')
        tsc_mode = tsc.get('mode')
        self.tsc_mode.set(tsc_mode if tsc_mode else 'None')

        self.tsc_frequency.delete(0, 'end')
        frequency = tsc.get('frequency')
        if frequency:
            self.tsc_frequency.insert(0, str(frequency))

        # HPET timer
        hpet = timers.get('hpet', {})
        hpet_present = hpet.get('present')
        self.hpet_present.set(hpet_present if hpet_present else 'None')

        # kvmclock timer
        kvmclock = timers.get('kvmclock', {})
        kvmclock_present = kvmclock.get('present')
        self.kvmclock_present.set(kvmclock_present if kvmclock_present else 'None')

    def _reset_to_none(self) -> None:
        """重置所有配置为 None."""
        self.offset.set('None')
        self.timezone.delete(0, 'end')
        self.adjustment.delete(0, 'end')
        self.basis.set('None')
        self.start.delete(0, 'end')

        self.rtc_present.set('None')
        self.rtc_tickpolicy.set('None')
        self.rtc_track.set('None')
        self.rtc_catchup_threshold.delete(0, 'end')
        self.rtc_catchup_slew.delete(0, 'end')
        self.rtc_catchup_limit.delete(0, 'end')

        self.pit_present.set('None')
        self.pit_tickpolicy.set('None')

        self.tsc_present.set('None')
        self.tsc_mode.set('None')
        self.tsc_frequency.delete(0, 'end')

        self.hpet_present.set('None')
        self.kvmclock_present.set('None')
