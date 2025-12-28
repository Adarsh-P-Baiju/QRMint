import customtkinter as ctk
from ...core.bank_manager import BankManager
from ..styles import Colors, Fonts, Dims
from ..components.bank_dialog import AddBankDialog

class BanksPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.manager = BankManager()
        
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=Dims.PAD_LG, pady=(Dims.PAD_LG, Dims.PAD_MD))
        
        ctk.CTkLabel(header_frame, text="Bank Accounts", font=Fonts.HEADER_LG, text_color=Colors.TEXT_MAIN).pack(side="left")
        
        ctk.CTkButton(header_frame, text="+ Add Bank", width=120, height=40, fg_color=Colors.SUCCESS,
                     text_color="white", hover_color="#00a844", command=self.add_bank).pack(side="right")
        
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True, padx=Dims.PAD_LG, pady=(0, Dims.PAD_MD))
        
        self.cards_frame = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        self.cards_frame.pack(fill="x", expand=True)
    
    def mount(self):
        """Called when page is shown"""
        self.load_banks()
    
    def load_banks(self):
        """Load and display all banks"""
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        
        banks = self.manager.get_all_banks()
        
        if not banks:
            ctk.CTkLabel(self.cards_frame, text="No bank accounts saved.\nClick '+ Add Bank' to get started.",
                        font=Fonts.BODY_LG, text_color=Colors.TEXT_MUTED).pack(pady=50)
            return
        
        for bank in banks:
            self.create_bank_card(bank)
    
    def create_bank_card(self, bank):
        """Create a card for a bank account"""
        card = ctk.CTkFrame(self.cards_frame, fg_color=Colors.BG_CARD, corner_radius=12)
        card.pack(fill="x", pady=6, padx=2)
        
        left = ctk.CTkFrame(card, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, padx=15, pady=12)
        
        name_row = ctk.CTkFrame(left, fg_color="transparent")
        name_row.pack(fill="x")
        
        ctk.CTkLabel(name_row, text=bank['bank_name'], font=("Outfit", 16, "bold"), 
                    text_color=Colors.TEXT_MAIN).pack(side="left")
        
        if bank['is_default']:
            badge = ctk.CTkLabel(name_row, text="DEFAULT", font=("Roboto", 10, "bold"),
                               text_color="white", fg_color=Colors.SUCCESS, corner_radius=4)
            badge.pack(side="left", padx=10, ipadx=6, ipady=2)
        
        ctk.CTkLabel(left, text=bank['vpa'], font=Fonts.BODY_SM, 
                    text_color=Colors.TEXT_MUTED, anchor="w").pack(fill="x", pady=(2, 0))
        
        ctk.CTkLabel(left, text=f"👤 {bank['account_holder']}", font=("Roboto", 12),
                    text_color=Colors.TEXT_MUTED, anchor="w").pack(fill="x", pady=(2, 0))
        
        right = ctk.CTkFrame(card, fg_color="transparent")
        right.pack(side="right", padx=15, pady=12)
        
        actions = ctk.CTkFrame(right, fg_color="transparent")
        actions.pack(anchor="e")
        
        if not bank['is_default']:
            ctk.CTkButton(actions, text="Set Default", width=80, height=30, fg_color=Colors.BG_MAIN,
                         text_color=Colors.PRIMARY, hover_color=Colors.BG_CARD_HOVER,
                         command=lambda: self.set_default(bank['id'])).pack(side="left", padx=2)
        
        ctk.CTkButton(actions, text="👁", width=32, height=32, fg_color=Colors.BG_MAIN,
                     text_color=Colors.TEXT_MAIN, hover_color=Colors.BG_CARD_HOVER,
                     command=lambda: self.view_details(bank)).pack(side="left", padx=2)
        
        ctk.CTkButton(actions, text="✏️", width=32, height=32, fg_color=Colors.BG_MAIN,
                     text_color=Colors.PRIMARY, hover_color=Colors.BG_CARD_HOVER,
                     command=lambda: self.edit_bank(bank)).pack(side="left", padx=2)
        
        ctk.CTkButton(actions, text="🗑", width=32, height=32, fg_color=Colors.ERROR,
                     text_color="white", hover_color="#c53030",
                     command=lambda: self.delete_bank(bank['id'], bank['bank_name'])).pack(side="left", padx=2)
    
    def add_bank(self):
        """Open dialog to add new bank"""
        AddBankDialog(self, self.on_bank_saved)
    
    def edit_bank(self, bank):
        """Open dialog to edit bank"""
        AddBankDialog(self, self.on_bank_updated, bank_data=bank)
    
    def on_bank_saved(self, data):
        """Callback when new bank is saved"""
        self.manager.add_bank(data['bank_name'], data['vpa'], data['account_holder'], data['is_default'])
        self.load_banks()
        
        from ..components.dialogs import CustomDialog
        CustomDialog.show_info(self, "Success", f"Bank '{data['bank_name']}' added successfully!")
    
    def on_bank_updated(self, data):
        """Callback when bank is updated"""
        self.manager.update_bank(data['id'], data['bank_name'], data['vpa'], data['account_holder'], data['is_default'])
        self.load_banks()
        
        from ..components.dialogs import CustomDialog
        CustomDialog.show_info(self, "Success", "Bank updated successfully!")
    
    def set_default(self, bank_id):
        """Set bank as default"""
        self.manager.set_default_bank(bank_id)
        self.load_banks()
    
    def view_details(self, bank):
        """Show detailed bank information"""
        from ..components.dialogs import CustomDialog
        details = f"""
Bank Name: {bank['bank_name']}
UPI ID: {bank['vpa']}
Account Holder: {bank['account_holder']}
Default: {'Yes' if bank['is_default'] else 'No'}
Created: {bank.get('created_at', 'N/A')}
        """
        CustomDialog.show_info(self, "Bank Details", details.strip())
    
    def delete_bank(self, bank_id, bank_name):
        """Delete a bank"""
        from ..components.dialogs import CustomDialog
        if CustomDialog.ask_yes_no(self, "Delete Bank", f"Delete '{bank_name}'?"):
            self.manager.delete_bank(bank_id)
            self.load_banks()
            CustomDialog.show_info(self, "Deleted", "Bank removed successfully!")
