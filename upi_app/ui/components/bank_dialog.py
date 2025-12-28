import customtkinter as ctk
from ..styles import Colors, Fonts, Dims

class AddBankDialog(ctk.CTkToplevel):
    def __init__(self, parent, callback, bank_data=None):
        super().__init__(parent)
        
        self.callback = callback
        self.bank_data = bank_data
        
        self.title("Add Bank Account" if not bank_data else "Edit Bank Account")
        self.geometry("500x450")
        self.configure(fg_color=Colors.BG_MAIN)
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self.after(100, self.create_ui)
        
    def create_ui(self):
        container = ctk.CTkFrame(self, fg_color=Colors.BG_CARD, corner_radius=12)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        header = ctk.CTkLabel(container, text="🏦 Bank Account Details", font=Fonts.HEADER_MD, text_color=Colors.TEXT_MAIN)
        header.pack(pady=(20, 10))
        
        scroll = ctk.CTkScrollableFrame(container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.bank_name_var = ctk.StringVar(value=self.bank_data['bank_name'] if self.bank_data else "")
        self.vpa_var = ctk.StringVar(value=self.bank_data['vpa'] if self.bank_data else "")
        self.holder_var = ctk.StringVar(value=self.bank_data['account_holder'] if self.bank_data else "")
        self.default_var = ctk.BooleanVar(value=bool(self.bank_data.get('is_default')) if self.bank_data else False)
        
        self.create_field(scroll, "Bank Name", self.bank_name_var, "e.g., HDFC Bank, Paytm")
        self.create_field(scroll, "UPI ID / VPA", self.vpa_var, "e.g., merchant@upi")
        self.create_field(scroll, "Account Holder", self.holder_var, "e.g., John Doe")
        
        check_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        check_frame.pack(fill="x", padx=20, pady=(10, 15))
        
        ctk.CTkCheckBox(check_frame, text="Set as Default Bank", variable=self.default_var,
                       font=Fonts.BODY_MD, text_color=Colors.TEXT_MAIN, fg_color=Colors.PRIMARY,
                       hover_color=Colors.PRIMARY_HOVER).pack(anchor="w")
        
        btn_row = ctk.CTkFrame(container, fg_color="transparent")
        btn_row.pack(fill="x", padx=30, pady=(0, 20))
        
        ctk.CTkButton(btn_row, text="Save", width=120, height=45, fg_color=Colors.SUCCESS,
                     hover_color="#00a844", font=("Roboto", 14, "bold"), command=self.save).pack(side="right")
        
        ctk.CTkButton(btn_row, text="Cancel", width=120, height=45, fg_color=Colors.BG_MAIN,
                     text_color=Colors.TEXT_MAIN, hover_color=Colors.BG_CARD_HOVER,
                     font=("Roboto", 14), command=self.destroy).pack(side="right", padx=(0, 10))
    
    def create_field(self, parent, label, variable, placeholder):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=30, pady=(0, 12))
        
        ctk.CTkLabel(frame, text=label, font=("Roboto", 12, "bold"), text_color=Colors.TEXT_MAIN).pack(anchor="w", pady=(0, 5))
        ctk.CTkEntry(frame, textvariable=variable, placeholder_text=placeholder, height=42,
                    border_width=1, border_color=Colors.BORDER, fg_color=Colors.BG_MAIN,
                    text_color=Colors.TEXT_MAIN, font=("Roboto", 13)).pack(fill="x")
    
    def save(self):
        from .dialogs import CustomDialog
        
        bank_name = self.bank_name_var.get().strip()
        vpa = self.vpa_var.get().strip()
        holder = self.holder_var.get().strip()
        
        if not bank_name or not vpa or not holder:
            CustomDialog.show_error(self, "Validation Error", "All fields are required!")
            return
        
        if "@" not in vpa:
            CustomDialog.show_error(self, "Validation Error", "Invalid VPA format!")
            return
        
        result = {
            'bank_name': bank_name,
            'vpa': vpa,
            'account_holder': holder,
            'is_default': self.default_var.get()
        }
        
        if self.bank_data:
            result['id'] = self.bank_data['id']
        
        self.callback(result)
        self.destroy()
