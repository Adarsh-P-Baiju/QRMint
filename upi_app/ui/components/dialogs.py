import customtkinter as ctk
from ..styles import Colors, Fonts, Dims

class CustomDialog(ctk.CTkToplevel):
    def __init__(self, master, title, message, type="info"):
        super().__init__(master)
        
        self.result = False
        self.type = type
        
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        transparent_color = "#000001"
        self.configure(fg_color=transparent_color)
        self.attributes("-transparentcolor", transparent_color)
        
        w, h = 420, 260
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")
        
        if type == "error":
            icon_text = "!"
            accent_color = Colors.ERROR
            btn_hover = "#cc3333"
        elif type == "confirm":
            icon_text = "?"
            accent_color = Colors.PRIMARY
            btn_hover = Colors.PRIMARY_HOVER
        elif type == "success":
            icon_text = "✓"
            accent_color = Colors.SUCCESS
            btn_hover = "#00a844"
        else:
            icon_text = "i"
            accent_color = Colors.INFO
            btn_hover = "#2897c2"

        self.card = ctk.CTkFrame(self, fg_color=Colors.BG_CARD, corner_radius=20, 
                                 border_width=2, border_color=Colors.BG_MAIN)
        self.card.pack(fill="both", expand=True)
        
        self.icon_frame = ctk.CTkFrame(self.card, width=60, height=60, corner_radius=30, fg_color=accent_color)
        self.icon_frame.pack(pady=(25, 15))
        self.icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(self.icon_frame, text=icon_text, font=("Roboto", 30, "bold"), text_color="white").place(relx=0.5, rely=0.5, anchor="center")
        
        self.title_lbl = ctk.CTkLabel(self.card, text=title, font=("Outfit", 20, "bold"), text_color=Colors.TEXT_MAIN)
        self.title_lbl.pack(pady=(0, 5))
        
        self.msg_lbl = ctk.CTkLabel(self.card, text=message, font=Fonts.BODY_MD, text_color=Colors.TEXT_MUTED, 
                                    wraplength=360, justify="center")
        self.msg_lbl.pack(pady=(0, 20), padx=30)
        
        self.btn_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.btn_frame.pack(fill="x", padx=30, pady=(0, 25), side="bottom")
        
        if type == "confirm":
            self.btn_frame.grid_columnconfigure((0, 1), weight=1, pad=15)
            
            ctk.CTkButton(self.btn_frame, text="Cancel", height=45, fg_color="transparent", 
                          border_width=1, border_color=Colors.BORDER, text_color=Colors.TEXT_MAIN,
                          font=("Roboto", 14, "bold"), hover_color=Colors.BG_MAIN,
                          command=self.on_cancel).grid(row=0, column=0, sticky="ew")
                          
            ctk.CTkButton(self.btn_frame, text="Confirm", height=45, fg_color=accent_color, 
                          text_color="white", font=("Roboto", 14, "bold"), hover_color=btn_hover,
                          command=self.on_ok).grid(row=0, column=1, sticky="ew")
        else:
            ctk.CTkButton(self.btn_frame, text="Okay", height=45, fg_color=accent_color,
                          text_color="white", font=("Roboto", 14, "bold"), hover_color=btn_hover,
                          command=self.on_ok).pack(fill="x")
                          
        self.grab_set()
        
        self.bind("<Return>", lambda e: self.on_ok())
        self.bind("<Escape>", lambda e: self.on_cancel())

    def on_ok(self):
        self.result = True
        self.destroy()
        
    def on_cancel(self):
        self.result = False
        self.destroy()

    @staticmethod
    def show_info(master, title, message):
        d = CustomDialog(master, title, message, "info")
        master.wait_window(d)

    @staticmethod
    def show_error(master, title, message):
        d = CustomDialog(master, title, message, "error")
        master.wait_window(d)

    @staticmethod
    def ask_yes_no(master, title, message):
        d = CustomDialog(master, title, message, "confirm")
        master.wait_window(d)
        return d.result
