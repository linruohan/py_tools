"""Home Panel"""

import customtkinter as ctk


class HomePanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.corner_radius = 0
        self.fg_color = "transparent"

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.init_ui()

    def init_ui(self):
        self.label = ctk.CTkLabel(self, text="Home Panel")
        self.label.grid(row=0, column=0, padx=20, pady=20)
