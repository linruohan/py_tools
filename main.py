"""Initialize the App class."""

from pathlib import Path

import customtkinter as ctk
from PIL import Image

from panels.home_panel import HomePanel
from panels.json_panel import JsonPanel


class App(ctk.CTk):
    """main app."""

    def __init__(self) -> None:
        """Initialize the App class."""
        super().__init__()
        self.title("py_tools")
        width = 800
        height = 450
        self.geometry(f"{width}x{height}")
        # self.eval("tk::PlaceWindow . center")
        self.center_window(width, height)

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        image_path = Path(__file__).resolve().parent / "test_images"
        self.logo_image = ctk.CTkImage(Image.open(image_path / "ctk_logo_single.png"), size=(15, 15))

        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(
            self.navigation_frame,
            text="  ctk_tools",
            image=self.logo_image,
            compound="left",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=0, pady=0)

        self.home_button = self.sidebar_btn(
            self.navigation_frame,
            name="Home",
            dark_image_name="home_dark",
            light_image_name="home_light",
            command=lambda: self.select_frame_by_name("home"),
            grid=(1, 0),
        )

        self.json_button = self.sidebar_btn(
            self.navigation_frame,
            name="json",
            dark_image_name="chat_dark",
            light_image_name="chat_light",
            command=lambda: self.select_frame_by_name("json"),
            grid=(2, 0),
        )

        self.frame_3_button = self.sidebar_btn(
            self.navigation_frame,
            name="Frame 3",
            dark_image_name="add_user_dark",
            light_image_name="add_user_light",
            command=lambda: self.select_frame_by_name("frame_3"),
            grid=(3, 0),
        )
        # create home frame
        self.home_panel = HomePanel(self)
        self.json_panel = JsonPanel(self)
        self.third_panel = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frame_mapping = {
            "home": (self.home_button, self.home_panel),
            "json": (self.json_button, self.json_panel),
            "frame_3": (self.frame_3_button, self.third_panel),
        }
        # select default frame
        self.select_frame_by_name("home")

    def icon(self, dark_image_name: str, light_image_name: str, size: tuple[int, int] = (20, 20)) -> ctk.CTkImage:
        """Create a CTkImage with dark and light images."""
        image_path = Path(__file__).resolve().parent / "test_images"
        return ctk.CTkImage(
            light_image=Image.open(image_path / f"{dark_image_name}.png"),
            dark_image=Image.open(image_path / f"{light_image_name}.png"),
            size=size,
        )

    def sidebar_btn(
        self,
        parent: ctk.CTkFrame,
        name: str,
        dark_image_name: str,
        light_image_name: str,
        command: callable,
        size: tuple[int, int] = (20, 20),
        grid: tuple[int, int] = (0, 0),
    ) -> ctk.CTkButton:
        """Create a sidebar button."""
        image = self.icon(dark_image_name=dark_image_name, light_image_name=light_image_name, size=size)
        btn = ctk.CTkButton(
            parent,
            corner_radius=0,
            height=25,
            border_spacing=5,
            text=name,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=image,
            anchor="w",
            command=command,
        )
        btn.grid(row=grid[0], column=grid[1], sticky="ew")
        return btn

    def center_window(self, width: int, height: int) -> None:
        """Center the window on the screen."""
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def select_frame_by_name(self, name: str) -> None:
        """Select frame by name."""
        for frame_name, (button, frame) in self.frame_mapping.items():
            button.configure(fg_color=("gray75", "gray25") if frame_name == name else "transparent")
            if frame_name == name:
                frame.grid(row=0, column=1, sticky="nsew")
            else:
                frame.grid_forget()


if __name__ == "__main__":
    app = App()
    app.mainloop()
