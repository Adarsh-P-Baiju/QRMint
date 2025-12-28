import customtkinter as ctk
from ..styles import Colors, Fonts

class CustomTitleBar(ctk.CTkFrame):
    def __init__(self, master, app_instance):
        super().__init__(master, height=40, fg_color=Colors.BG_CARD, corner_radius=0)
        self.app = app_instance
        self.pack_propagate(False)
        
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(side="left", fill="y", padx=15)
        
        ctk.CTkLabel(title_frame, text="💠", font=("Roboto", 20)).pack(side="left", padx=(0, 5))
        ctk.CTkLabel(title_frame, text="QRMint", font=("Outfit", 16, "bold"), 
                    text_color=Colors.TEXT_MAIN).pack(side="left")
        
        ctk.CTkLabel(title_frame, text="(Ctrl+Shift+R to restore)", font=("Roboto", 9), 
                    text_color=Colors.TEXT_MUTED).pack(side="left", padx=10)
        
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(side="right", padx=5)
        
        ctk.CTkButton(controls, text="—", width=40, height=30, fg_color="transparent",
                     text_color=Colors.TEXT_MAIN, hover_color=Colors.BG_MAIN,
                     command=self.minimize, font=("Roboto", 16, "bold")).pack(side="left", padx=2)
        
        self.max_btn = ctk.CTkButton(controls, text="□", width=40, height=30, fg_color="transparent",
                                     text_color=Colors.TEXT_MAIN, hover_color=Colors.BG_MAIN,
                                     command=self.toggle_maximize, font=("Roboto", 14))
        self.max_btn.pack(side="left", padx=2)
        
        ctk.CTkButton(controls, text="✕", width=40, height=30, fg_color="transparent",
                     text_color=Colors.ERROR, hover_color="#fee",
                     command=self.close, font=("Roboto", 16)).pack(side="left", padx=2)
        
        self.bind("<Button-1>", self.start_move)
        self.bind("<B1-Motion>", self.on_move)
        title_frame.bind("<Button-1>", self.start_move)
        title_frame.bind("<B1-Motion>", self.on_move)
        
        self.is_maximized = False
        self.normal_geometry = None
    
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
    
    def on_move(self, event):
        if self.is_maximized:
            self.toggle_maximize()
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.app.winfo_x() + deltax
        y = self.app.winfo_y() + deltay
        self.app.geometry(f"+{x}+{y}")
    
    def minimize(self):
        self.app.iconify()
    
    def toggle_maximize(self):
        if self.is_maximized:
            if self.normal_geometry:
                self.app.geometry(self.normal_geometry)
            self.max_btn.configure(text="□")
            self.is_maximized = False
        else:
            self.normal_geometry = self.app.geometry()
            screen_width = self.app.winfo_screenwidth()
            screen_height = self.app.winfo_screenheight()
            self.app.geometry(f"{screen_width}x{screen_height}+0+0")
            self.max_btn.configure(text="❐")
            self.is_maximized = True
    
    def close(self):
        self.app.confirm_exit(None)
