import customtkinter as ctk
from tkinter import filedialog, messagebox
from ...core.settings_manager import SettingsManager
from ..styles import Fonts, Colors, Dims
from ..components.loader import Loader
from ...core.auth_manager import AuthManager
import shutil
import os

class SettingsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.settings_manager = SettingsManager()
        self.auth_manager = AuthManager()
        
        self.loader = Loader(self, width=60, height=60)
        self.loader.place(relx=0.5, rely=0.5, anchor="center")
        self.loader.lower()

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True)

        self.container = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.container.pack(expand=True, fill="both", padx=Dims.PAD_LG, pady=Dims.PAD_LG)
        
        head = ctk.CTkFrame(self.container, fg_color="transparent")
        head.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(head, text="Settings & Preferences", font=Fonts.HEADER_LG, text_color=Colors.TEXT_MAIN).pack(side="left")

        self.storage_card = ctk.CTkFrame(self.container, fg_color=Colors.BG_CARD, corner_radius=Dims.CORNER_RADIUS)
        self.storage_card.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(self.storage_card, text="Storage Configuration", font=Fonts.HEADER_SM, text_color=Colors.TEXT_MAIN).pack(anchor="w", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(self.storage_card, text="Default Save Directory", font=Fonts.BODY_SM, text_color=Colors.TEXT_MUTED).pack(anchor="w", padx=20, pady=(0, 5))
        
        self.path_frame = ctk.CTkFrame(self.storage_card, fg_color=Colors.BG_MAIN, border_color=Colors.BORDER, border_width=1, corner_radius=8)
        self.path_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.path_lbl = ctk.CTkLabel(self.path_frame, text="Not Set", font=Fonts.BODY_MD, text_color=Colors.TEXT_MAIN)
        self.path_lbl.pack(side="left", padx=15, pady=10)
        
        ctk.CTkButton(self.path_frame, text="Change Folder", command=self.select_dir, width=120, height=32,
                      fg_color=Colors.PRIMARY, hover_color=Colors.PRIMARY_HOVER).pack(side="right", padx=10, pady=5)
        
        self.defaults_card = ctk.CTkFrame(self.container, fg_color=Colors.BG_CARD, corner_radius=Dims.CORNER_RADIUS)
        self.defaults_card.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(self.defaults_card, text="Default Credentials", font=Fonts.HEADER_SM, text_color=Colors.TEXT_MAIN).pack(anchor="w", padx=20, pady=(20, 10))
        ctk.CTkLabel(self.defaults_card, text="Pre-fill these values when generating QRs manually.", font=Fonts.BODY_SM, text_color=Colors.TEXT_MUTED).pack(anchor="w", padx=20, pady=(0, 20))
        
        self.vpa_var = ctk.StringVar()
        self.name_var = ctk.StringVar()
        
        self.create_input(self.defaults_card, "Default VPA / UPI ID", self.vpa_var, placeholder="e.g. merchant@banks")
        self.create_input(self.defaults_card, "Default Payee Name", self.name_var, placeholder="e.g. My Business")
        
        save_btn = ctk.CTkButton(self.defaults_card, text="Save Defaults", command=self.save_creds, height=45,
                                 fg_color=Colors.SUCCESS, hover_color=Colors.SUCCESS, font=("Roboto", 14, "bold"))
        save_btn.pack(anchor="e", padx=20, pady=(10, 20))
        
        self.data_card = ctk.CTkFrame(self.container, fg_color=Colors.BG_CARD, corner_radius=Dims.CORNER_RADIUS)
        self.data_card.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(self.data_card, text="Data Management", font=Fonts.HEADER_SM, text_color=Colors.TEXT_MAIN).pack(anchor="w", padx=20, pady=(20, 10))
        ctk.CTkLabel(self.data_card, text="Backup or restore your application database.", font=Fonts.BODY_SM, text_color=Colors.TEXT_MUTED).pack(anchor="w", padx=20, pady=(0, 20))
        
        btn_frame = ctk.CTkFrame(self.data_card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(btn_frame, text="Backup Database", command=self.backup_db, width=150, height=40,
                      fg_color=Colors.PRIMARY, hover_color=Colors.PRIMARY_HOVER).pack(side="left", padx=(0, 10))
                      
        ctk.CTkButton(btn_frame, text="Restore Database", command=self.restore_db, width=150, height=40,
                      fg_color=Colors.ERROR, hover_color="#c0392b").pack(side="left")

        self.sec_card = ctk.CTkFrame(self.container, fg_color=Colors.BG_CARD, corner_radius=Dims.CORNER_RADIUS)
        self.sec_card.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(self.sec_card, text="Security", font=Fonts.HEADER_SM, text_color=Colors.TEXT_MAIN).pack(anchor="w", padx=20, pady=(20, 10))
        ctk.CTkLabel(self.sec_card, text="Change your application password.", font=Fonts.BODY_SM, text_color=Colors.TEXT_MUTED).pack(anchor="w", padx=20, pady=(0, 15))
        
        self.pw_old = ctk.StringVar()
        self.pw_new = ctk.StringVar()
        
        self.create_input(self.sec_card, "Current Password", self.pw_old, placeholder="Required")
        self.create_input(self.sec_card, "New Password", self.pw_new, placeholder="Minimum 4 characters")
        
        ctk.CTkButton(self.sec_card, text="Update Password", command=self.update_password, height=40,
                      fg_color=Colors.PRIMARY, hover_color=Colors.PRIMARY_HOVER).pack(anchor="e", padx=20, pady=(5, 20))

        self.about_card = ctk.CTkFrame(self.container, fg_color=Colors.BG_CARD, corner_radius=Dims.CORNER_RADIUS)
        self.about_card.pack(fill="x")
        
        ctk.CTkLabel(self.about_card, text="About Application", font=Fonts.HEADER_SM, text_color=Colors.TEXT_MAIN).pack(anchor="w", padx=20, pady=(20, 5))
        ctk.CTkLabel(self.about_card, text="UPI Forge Enterprise v2.1\nDesigned for speed, aesthetics, and reliability.", 
                     font=Fonts.BODY_MD, text_color=Colors.TEXT_MUTED, justify="left").pack(anchor="w", padx=20, pady=(0, 20))
        
        self.mount()

    def mount(self):
        current_dir = self.settings_manager.default_save_dir
        if current_dir:
            self.path_lbl.configure(text=current_dir)
        else:
            self.path_lbl.configure(text="No default folder set")
            
        self.vpa_var.set(self.settings_manager.default_vpa)
        self.name_var.set(self.settings_manager.default_name)

    def select_dir(self):
        from ..components.dialogs import CustomDialog
        path = filedialog.askdirectory()
        if path:
            self.settings_manager.default_save_dir = path
            self.mount()
            CustomDialog.show_info(self, "Saved", "Directory updated successfully.")

    def create_input(self, parent, label, var, placeholder=""):
        ctk.CTkLabel(parent, text=label, font=Fonts.BODY_SM, text_color=Colors.TEXT_MUTED).pack(anchor="w", padx=20, pady=(5, 5))
        entry = ctk.CTkEntry(parent, textvariable=var, border_color=Colors.BORDER, width=400, height=40,
                             fg_color=Colors.BG_MAIN, text_color=Colors.TEXT_MAIN, placeholder_text=placeholder)
        entry.pack(anchor="w", padx=20, pady=(0, 15))

    def save_creds(self):
        self.loader.lift()
        self.loader.start()
        self.after(400, self._save_logic)
        
    def _save_logic(self):
        from ..components.dialogs import CustomDialog
        self.settings_manager.default_vpa = self.vpa_var.get().strip()
        self.settings_manager.default_name = self.name_var.get().strip()
        self.loader.lower()
        CustomDialog.show_info(self, "Saved", "Default credentials updated.")

    def backup_db(self):
        from ..components.dialogs import CustomDialog
        src = "upi_app.db"
        if not os.path.exists(src):
            CustomDialog.show_error(self, "Error", "Database file not found!")
            return
            
        dst = filedialog.asksaveasfilename(
            defaultextension=".db",
            initialfile=f"backup_upi_app_{os.path.basename(os.getcwd())}.db",
            filetypes=[("SQLite Database", "*.db")]
        )
        
        if dst:
            try:
                shutil.copy2(src, dst)
                CustomDialog.show_info(self, "Success", f"Backup successfully saved to:\n{dst}")
            except Exception as e:
                CustomDialog.show_error(self, "Backup Failed", str(e))

    def restore_db(self):
        from ..components.dialogs import CustomDialog
        if not CustomDialog.ask_yes_no(self, "Confirm Restore", "Restoring a database will OVERWRITE your current data.\n\nAre you sure you want to proceed?"):
            return
            
        src = filedialog.askopenfilename(filetypes=[("SQLite Database", "*.db")])
        if not src: return
        
        try:
            if not os.path.exists(src): raise FileNotFoundError("Selected file does not exist.")
            
            shutil.copy2(src, "upi_app.db")
            
            CustomDialog.show_info(self, "Success", "Database restored successfully!\n\nPlease restart the application to apply changes.")
        except Exception as e:
            CustomDialog.show_error(self, "Restore Failed", str(e))

    def update_password(self):
        from ..components.dialogs import CustomDialog
        old = self.pw_old.get().strip()
        new = self.pw_new.get().strip()
        
        if not old or not new:
            CustomDialog.show_error(self, "Input", "Please fill both password fields.")
            return
            
        if len(new) < 4:
            CustomDialog.show_error(self, "Weak Password", "New password must be at least 4 characters.")
            return

        if not self.auth_manager.verify_password(old):
            CustomDialog.show_error(self, "Error", "Incorrect current password.")
            return
            
        if self.auth_manager.set_password(new):
            CustomDialog.show_info(self, "Success", "Password updated successfully!")
            self.pw_old.set("")
            self.pw_new.set("")
        else:
            CustomDialog.show_error(self, "Error", "Failed to update password.")
