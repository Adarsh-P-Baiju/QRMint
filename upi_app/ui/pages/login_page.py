import customtkinter as ctk
from tkinter import messagebox
from ...core.auth_manager import AuthManager
from ..styles import Colors, Fonts

class LoginPage(ctk.CTkFrame):
    def __init__(self, master, on_login_success, app_instance=None):
        super().__init__(master, fg_color=Colors.BG_MAIN)
        self.auth = AuthManager()
        self.on_login_success = on_login_success
        self.app_instance = app_instance if app_instance else master
        self.is_setup = not self.auth.is_setup_completed()
        
        self.center_frame = ctk.CTkFrame(self, fg_color=Colors.BG_CARD, corner_radius=16, width=400, height=350)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.center_frame.pack_propagate(False)
        
        ctk.CTkLabel(self.center_frame, text="🔒", font=("Emoji", 48)).pack(pady=(40, 10))
        
        title = "Setup Password" if self.is_setup else "Login Required"
        ctk.CTkLabel(self.center_frame, text=title, font=Fonts.HEADER_LG, text_color=Colors.TEXT_MAIN).pack(pady=(0, 20))
        
        self.pwd_entry = ctk.CTkEntry(self.center_frame, placeholder_text="Enter Password", show="*", 
                                      width=280, height=45, border_color=Colors.PRIMARY,
                                      fg_color=Colors.BG_MAIN, text_color=Colors.TEXT_MAIN)
        self.pwd_entry.pack(pady=10)
        self.pwd_entry.bind("<Return>", lambda e: self.attempt_login())
        
        btn_text = "Create Admin" if self.is_setup else "Unlock"
        ctk.CTkButton(self.center_frame, text=btn_text, command=self.attempt_login,
                      width=280, height=45, fg_color=Colors.PRIMARY, hover_color=Colors.PRIMARY_HOVER,
                      font=("Outfit", 14, "bold")).pack(pady=20)
                      
        ctk.CTkButton(self.center_frame, text="Exit Application", command=self.app_instance.confirm_exit,
                      fg_color="transparent", hover_color=Colors.BG_MAIN, text_color=Colors.ERROR, 
                      width=280, height=30).pack(pady=(0, 20))
                      
    def attempt_login(self):
        from ..components.dialogs import CustomDialog
        pwd = self.pwd_entry.get().strip()
        if not pwd:
            CustomDialog.show_error(self, "Input Error", "Password cannot be empty.")
            return
            
        if self.is_setup:
            if self.auth.set_password(pwd):
                CustomDialog.show_info(self, "Setup Complete", "Password set successfully!")
                self.on_login_success()
            else:
                CustomDialog.show_error(self, "Database Error", "Failed to save password.")
        else:
            if self.auth.verify_password(pwd):
                self.on_login_success()
            else:
                CustomDialog.show_error(self, "Access Denied", "Incorrect Password.")
                self.pwd_entry.delete(0, 'end')
