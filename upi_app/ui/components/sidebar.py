import customtkinter as ctk
from ..styles import Colors, Fonts, Dims

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, on_navigate, app_instance=None):
        super().__init__(master, width=240, corner_radius=0, fg_color=Colors.BG_CARD, border_width=0)
        self.on_navigate = on_navigate
        self.app_instance = app_instance if app_instance else master
        self.buttons = {}
        self.is_collapsed = False
        
        self.grid_propagate(False)
        
        self.brand_frame = ctk.CTkFrame(self, fg_color="transparent", height=90)
        self.brand_frame.pack(fill="x", pady=(20, 10))
        self.brand_frame.pack_propagate(False)
        
        self.logo_btn = ctk.CTkButton(self.brand_frame, text="💠", font=("Roboto", 28), 
                                      fg_color="transparent", hover=False, width=60, 
                                      text_color=Colors.PRIMARY, command=self.toggle_collapse)
        self.logo_btn.pack(side="left", padx=(10, 0))
        
        self.title_lbl = ctk.CTkLabel(self.brand_frame, text="QRMint", font=("Outfit", 26, "bold"), text_color=Colors.TEXT_MAIN)
        self.title_lbl.pack(side="left", padx=5)
        
        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_frame.pack(fill="both", expand=True, padx=10)
        
        self.items = [
            ("dashboard", "Dashboard", "📊"),
            ("generator", "Generator", "⚡"),
            ("templates", "Templates", "📝"),
            ("batch", "Batch Ops", "📦"),
            ("history", "History", "📜"),
            ("banks", "Banks", "🏦"),
            ("settings", "Settings", "⚙️")
        ]
        
        for key, lbl, icon in self.items:
            self.create_nav_btn(key, lbl, icon)
            
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(fill="x", padx=10, pady=20)
        ctk.CTkButton(footer, text="Exit App", fg_color=Colors.ERROR, hover_color="#c53030", 
                      height=30, width=100, command=self.app_instance.confirm_exit).pack(pady=(0, 10))
                      
        self.ver_lbl = ctk.CTkLabel(footer, text="v2.1 Enterprise", font=Fonts.BODY_SM, text_color=Colors.TEXT_MUTED)
        self.ver_lbl.pack()

    def create_nav_btn(self, key, label, icon):
        btn = ctk.CTkButton(self.nav_frame, text=f"  {icon}   {label}", anchor="w",
                            font=("Roboto", 14, "bold"), height=48, corner_radius=12,
                            fg_color="transparent", text_color=Colors.TEXT_MUTED,
                            hover_color=Colors.BG_MAIN,
                            command=lambda k=key: self.handle_nav(k))
        btn.pack(fill="x", pady=4)
        self.buttons[key] = btn

    def handle_nav(self, key):
        self.on_navigate(key)
        for k, b in self.buttons.items():
            if k == key:
                b.configure(fg_color=Colors.BG_MAIN, text_color=Colors.PRIMARY)
            else:
                b.configure(fg_color="transparent", text_color=Colors.TEXT_MUTED)

    def toggle_collapse(self):
        self.is_collapsed = not self.is_collapsed
        self.update_width()

    def update_width(self):
        w = 70 if self.is_collapsed else 240
        self.configure(width=w)
        
        if self.is_collapsed:
            self.title_lbl.pack_forget()
            self.ver_lbl.pack_forget()
            for key, lbl, icon in self.items:
                self.buttons[key].configure(text=icon, anchor="center")
        else:
            self.title_lbl.pack(side="left", padx=5)
            self.ver_lbl.pack()
            for key, lbl, icon in self.items:
                self.buttons[key].configure(text=f"  {icon}   {lbl}", anchor="w")
