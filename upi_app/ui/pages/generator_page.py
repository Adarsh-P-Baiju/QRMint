import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime
from ...core.qr_generator import UPIQRGenerator
from ...core.template_manager import TemplateManager
from ..styles import Fonts, Colors, Dims
from ..components.loader import Loader

class GeneratorPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        self.qr_gen = UPIQRGenerator()
        self.tpl_manager = TemplateManager()
        self.logo_path = None
        self.preview_image = None
        
        self.loader = Loader(self, width=80, height=80)
        self.loader.place(relx=0.5, rely=0.5, anchor="center")
        self.loader.lower()

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True)

        self.container = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.container.pack(fill="x", padx=Dims.PAD_LG, pady=Dims.PAD_LG)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        
        self.form_card = ctk.CTkFrame(self.container, fg_color=Colors.BG_CARD, corner_radius=Dims.CORNER_RADIUS)
        self.form_card.grid(row=0, column=0, sticky="nsew", padx=(0, Dims.PAD_MD), pady=(0, 20))
        
        head = ctk.CTkFrame(self.form_card, fg_color="transparent")
        head.pack(fill="x", padx=Dims.PAD_LG, pady=(Dims.PAD_LG, Dims.PAD_MD))
        ctk.CTkLabel(head, text="Generate QR Code", font=Fonts.HEADER_LG, text_color=Colors.TEXT_MAIN).pack(side="left")
        
        top_actions = ctk.CTkFrame(head, fg_color="transparent")
        top_actions.pack(side="right")
        
        ctk.CTkButton(top_actions, text="🎨 Design", width=80, height=32, fg_color=Colors.BG_MAIN, 
                      text_color=Colors.TEXT_MAIN, hover_color=Colors.BG_CARD_HOVER, command=self.open_design_drawer).pack(side="left", padx=(0, 10))

        ctk.CTkButton(top_actions, text="📂 Templates", width=100, height=32, fg_color=Colors.BG_MAIN, 
                      text_color=Colors.PRIMARY, hover_color=Colors.BG_CARD_HOVER, command=self.open_template_drawer).pack(side="left")
        
        ctk.CTkLabel(head, text="Create standard UPI QRs instantly", font=Fonts.BODY_SM, text_color=Colors.TEXT_MUTED).place(x=0, y=35)
        
        
        ctk.CTkLabel(self.form_card, text="Select Bank Account", font=Fonts.BODY_SM, text_color=Colors.TEXT_MAIN).pack(anchor="w", padx=Dims.PAD_LG, pady=(10, 5))
        
        bank_row = ctk.CTkFrame(self.form_card, fg_color="transparent")
        bank_row.pack(fill="x", padx=Dims.PAD_LG, pady=(0, 10))
        
        self.bank_var = ctk.StringVar(value="Manual Entry")
        self.bank_dropdown = ctk.CTkOptionMenu(bank_row, variable=self.bank_var, values=["Manual Entry"],
                                               fg_color=Colors.BG_MAIN, button_color=Colors.PRIMARY, text_color=Colors.TEXT_MAIN,
                                               height=40, command=self.on_bank_selected)
        self.bank_dropdown.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(bank_row, text="+ Add Bank", width=100, height=40, fg_color=Colors.SUCCESS, 
                     text_color="white", hover_color="#00a844", command=self.add_new_bank).pack(side="right")
        
        self.vpa_frame = ctk.CTkFrame(self.form_card, fg_color="transparent")
        self.vpa_frame.pack(fill="x")
        
        self.create_input(self.vpa_frame, "UPI ID / VPA *", "vpa_entry", placeholder="e.g. merchant@upi")
        self.create_input(self.vpa_frame, "Payee Name *", "name_entry", placeholder="e.g. Store Name")
        
        self.create_input(self.form_card, "Amount (Optional)", "amount_entry", placeholder="e.g. 1000")
        self.create_input(self.form_card, "Note / Reference", "note_entry", placeholder="e.g. Bill
        
        self.create_logo_picker(self.form_card)
        
        ctk.CTkLabel(self.form_card, text="Initial Payment Status", font=Fonts.BODY_SM, text_color=Colors.TEXT_MAIN).pack(anchor="w", padx=Dims.PAD_LG, pady=(10, 5))
        self.status_var = ctk.StringVar(value="Unpaid")
        self.status_menu = ctk.CTkOptionMenu(self.form_card, variable=self.status_var, values=["Paid", "Unpaid", "Pending"],
                                             fg_color=Colors.BG_MAIN, button_color=Colors.PRIMARY, text_color=Colors.TEXT_MAIN, height=35)
        self.status_menu.pack(fill="x", padx=Dims.PAD_LG, pady=(0, 20))

        btn_frame = ctk.CTkFrame(self.form_card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=Dims.PAD_LG, pady=(0, Dims.PAD_LG))
        
        self.gen_btn = ctk.CTkButton(btn_frame, text="⚡ Generate Preview", command=self.generate_preview, 
                                     font=("Roboto", 14, "bold"), height=48, fg_color=Colors.PRIMARY, hover_color=Colors.PRIMARY_HOVER, corner_radius=12)
        self.gen_btn.pack(fill="x", pady=(0, 10))
        
        ctk.CTkButton(btn_frame, text="💾 Save Current as Template", command=self.save_as_template,
                      fg_color="transparent", text_color=Colors.TEXT_MUTED, hover_color=Colors.BG_MAIN, height=30).pack(fill="x")
        
        self.preview_card = ctk.CTkFrame(self.container, fg_color=Colors.BG_CARD, corner_radius=Dims.CORNER_RADIUS)
        self.preview_card.grid(row=0, column=1, sticky="nsew", pady=(0, 20))
        
        ctk.CTkLabel(self.preview_card, text="Live Preview", font=Fonts.HEADER_MD, text_color=Colors.TEXT_MAIN).pack(pady=Dims.PAD_LG)
        
        self.preview_box = ctk.CTkFrame(self.preview_card, width=300, height=300, fg_color=Colors.BG_MAIN, corner_radius=Dims.CORNER_RADIUS)
        self.preview_box.pack(expand=True, padx=20, pady=20)
        self.preview_box.pack_propagate(False)
        
        self.qr_lbl = ctk.CTkLabel(self.preview_box, text="Enter details to generate", text_color=Colors.TEXT_MUTED)
        self.qr_lbl.place(relx=0.5, rely=0.5, anchor="center")
        
        self.actions_frame = ctk.CTkFrame(self.preview_card, fg_color="transparent")
        self.actions_frame.pack(fill="x", padx=Dims.PAD_LG, pady=Dims.PAD_LG)
        
        self.history_btn = ctk.CTkButton(self.actions_frame, text="💾 Save Record", command=self.save_to_history,
                                       font=Fonts.BODY_MD, height=40, fg_color=Colors.SUCCESS, hover_color="#00a844", state="disabled")
        self.history_btn.pack(fill="x", pady=(0, 10))

        self.link_btn = ctk.CTkButton(self.actions_frame, text="🔗 Copy Payment Link", command=self.copy_upi_link, 
                                      font=Fonts.BODY_MD, height=40, fg_color=Colors.INFO, hover_color="#2897c2", state="disabled")
        self.link_btn.pack(fill="x", pady=(0, 10))
        
        self.download_btn = ctk.CTkButton(self.actions_frame, text="📥 Download PNG", command=self.download_image, 
                                       font=Fonts.BODY_MD, height=40, fg_color=Colors.BG_CARD, hover_color=Colors.BG_CARD_HOVER,
                                       text_color=Colors.TEXT_MAIN, border_width=1, border_color=Colors.BORDER, state="disabled")
        self.download_btn.pack(fill="x")

    def create_input(self, parent, label, attr_name, placeholder=""):
        ctk.CTkLabel(parent, text=label, font=Fonts.BODY_SM, text_color=Colors.TEXT_MUTED).pack(anchor="w", padx=Dims.PAD_LG, pady=(5, 5))
        entry = ctk.CTkEntry(parent, height=45, border_width=1, border_color=Colors.BORDER, corner_radius=10,
                             fg_color=Colors.BG_MAIN, text_color=Colors.TEXT_MAIN, placeholder_text=placeholder)
        entry.pack(fill="x", padx=Dims.PAD_LG, pady=(0, 10))
        setattr(self, attr_name, entry)

    def create_logo_picker(self, parent):
        ctk.CTkLabel(parent, text="Center Logo (Optional)", font=Fonts.BODY_SM, text_color=Colors.TEXT_MUTED).pack(anchor="w", padx=Dims.PAD_LG, pady=(5, 5))
        
        self.logo_frame = ctk.CTkFrame(parent, fg_color=Colors.BG_MAIN, border_width=1, border_color=Colors.BORDER, height=45, corner_radius=10)
        self.logo_frame.pack(fill="x", padx=Dims.PAD_LG, pady=(0, 10))
        self.logo_frame.pack_propagate(False)
        
        self.logo_lbl = ctk.CTkLabel(self.logo_frame, text="No file selected", font=Fonts.BODY_SM, text_color=Colors.TEXT_MUTED)
        self.logo_lbl.pack(side="left", padx=15)
        
        ctk.CTkButton(self.logo_frame, text="Browse", width=80, height=30, fg_color=Colors.BG_CARD, text_color=Colors.TEXT_MAIN, 
                      hover_color=Colors.BG_CARD_HOVER, command=self.select_logo).pack(side="right", padx=10)

    def select_logo(self):
        from ..components.dialogs import CustomDialog
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
        if path:
            import shutil
            
            media_dir = os.path.join(os.getcwd(), "media")
            os.makedirs(media_dir, exist_ok=True)
            
            filename = f"logo_{int(datetime.now().timestamp())}{os.path.splitext(path)[1]}"
            dest_path = os.path.join(media_dir, filename)
            
            try:
                shutil.copy2(path, dest_path)
                self.logo_path = dest_path
                self.logo_lbl.configure(text=filename, text_color=Colors.TEXT_MAIN)
            except Exception as e:
                CustomDialog.show_error(self, "Error", f"Failed to save logo: {e}")
                self.logo_path = path

    def mount(self):
        from ...core.settings_manager import SettingsManager
        from ...core.bank_manager import BankManager
        
        self.bank_manager = BankManager()
        banks = self.bank_manager.get_all_banks()
        
        bank_options = ["Manual Entry"]
        self.bank_map = {}
        
        for bank in banks:
            option_text = f"🏦 {bank['bank_name']}"
            bank_options.append(option_text)
            self.bank_map[option_text] = bank
        
        self.bank_dropdown.configure(values=bank_options)
        
        default_bank = self.bank_manager.get_default_bank()
        if default_bank:
            default_text = f"🏦 {default_bank['bank_name']}"
            self.bank_var.set(default_text)
            self.on_bank_selected(default_text)
        else:
            settings = SettingsManager()
            if not self.vpa_entry.get(): self.vpa_entry.insert(0, settings.default_vpa)
            if not self.name_entry.get(): self.name_entry.insert(0, settings.default_name)
        
        if not hasattr(self, 'fg_color'): self.fg_color = "black"
        if not hasattr(self, 'bg_color'): self.bg_color = "white"
    
    def on_bank_selected(self, selected):
        """Handle bank selection from dropdown"""
        if selected == "Manual Entry":
            self.vpa_entry.delete(0, 'end')
            self.name_entry.delete(0, 'end')
        elif selected in self.bank_map:
            bank = self.bank_map[selected]
            self.vpa_entry.delete(0, 'end')
            self.vpa_entry.insert(0, bank['vpa'])
            self.name_entry.delete(0, 'end')
            self.name_entry.insert(0, bank['account_holder'])
    
    def add_new_bank(self):
        """Open dialog to add new bank"""
        from ..components.bank_dialog import AddBankDialog
        AddBankDialog(self, self.on_new_bank_saved)
    
    def on_new_bank_saved(self, data):
        """Callback when new bank is added"""
        bank_id = self.bank_manager.add_bank(data['bank_name'], data['vpa'], data['account_holder'], data['is_default'])
        
        from ..components.dialogs import CustomDialog
        CustomDialog.show_info(self, "Success", f"Bank '{data['bank_name']}' added!")
        
        self.mount()

    def generate_preview(self):
        from ..components.dialogs import CustomDialog
        vpa = self.vpa_entry.get().strip()
        name = self.name_entry.get().strip()
        amount = self.amount_entry.get().strip()
        note = self.note_entry.get().strip()
        
        if not vpa or not name:
            CustomDialog.show_error(self, "Validation Error", "VPA and Name are required!")
            return
            
        self.loader.lift()
        self.loader.start()
        
        if not hasattr(self, 'fg_color'): self.fg_color = "black"
        if not hasattr(self, 'bg_color'): self.bg_color = "white"
            
        self.after(500, lambda: self._generate_logic(vpa, name, amount, note))

    def _generate_logic(self, vpa, name, amount, note):
        from ..components.dialogs import CustomDialog
        try:
            pil_img = self.qr_gen.generate_qr(vpa, name, amount, note, logo_path=self.logo_path, 
                                            fg_color=self.fg_color, bg_color=self.bg_color)
            self.preview_image = pil_img
            
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(280, 280))
            self.qr_lbl.configure(image=ctk_img, text="")
            
            self.history_btn.configure(state="normal")
            self.download_btn.configure(state="normal")
            self.link_btn.configure(state="normal")
        except Exception as e:
            CustomDialog.show_error(self, "Generation Failed", str(e))
        finally:
            self.loader.stop()
            self.loader.lower()
            
    def copy_upi_link(self):
        from ..components.dialogs import CustomDialog
        try:
            vpa = self.vpa_entry.get()
            name = self.name_entry.get()
            amount = self.amount_entry.get()
            note = self.note_entry.get()
            
            link = self.qr_gen.generate_upi_link(vpa, name, amount, note)
            
            self.clipboard_clear()
            self.clipboard_append(link)
            self.update()
            
            CustomDialog.show_info(self, "Copied", "Payment link copied to clipboard!")
        except Exception as e:
             CustomDialog.show_error(self, "Error", str(e))

    def open_design_drawer(self):
        self.drawer_design = ctk.CTkFrame(self, fg_color=Colors.BG_CARD, width=350)
        self.drawer_design.place(relx=1, rely=0, relwidth=0.4, relheight=1, anchor="ne")
        self.drawer_design.lift()
        
        h = ctk.CTkFrame(self.drawer_design, fg_color="transparent", height=60)
        h.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(h, text="Design Studio", font=("Outfit", 20, "bold"), text_color=Colors.TEXT_MAIN).pack(side="left")
        ctk.CTkButton(h, text="✕", width=40, fg_color="transparent", text_color=Colors.TEXT_MAIN,
                      hover_color=Colors.BG_MAIN, command=self.drawer_design.destroy).pack(side="right")
                      
        scroll = ctk.CTkScrollableFrame(self.drawer_design, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20)
        
        ctk.CTkLabel(scroll, text="Color Presets", font=Fonts.HEADER_SM, text_color=Colors.TEXT_MAIN).pack(anchor="w", pady=(10, 10))
        
        presets = [
            ("Classic", "black", "white"),
            ("Brand Blue", Colors.PRIMARY, "white"),
            ("Eco Green", Colors.SUCCESS, "white"),
            ("Royal Purple", "#8e44ad", "white"),
            ("Dark Mode", "white", "#1e1e1e"),
            ("Gold", "#f1c40f", "#2c3e50")
        ]
        
        p_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        p_frame.pack(fill="x")
        
        for i, (name, fg, bg) in enumerate(presets):
            btn = ctk.CTkButton(p_frame, text=name, fg_color=fg, hover_color=fg, text_color=bg, 
                                height=40, command=lambda f=fg, b=bg: self.apply_color(f, b))
            btn.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="ew")
            
        p_frame.grid_columnconfigure((0, 1), weight=1)
        
        ctk.CTkLabel(scroll, text="Custom Hex Colors", font=Fonts.HEADER_SM, text_color=Colors.TEXT_MAIN).pack(anchor="w", pady=(20, 10))
        
        self.fg_entry = ctk.CTkEntry(scroll, placeholder_text="Foreground (e.g.
        self.fg_entry.pack(fill="x", pady=5)
        self.fg_entry.insert(0, getattr(self, 'fg_color', 'black'))
        
        self.bg_entry = ctk.CTkEntry(scroll, placeholder_text="Background (e.g. white)")
        self.bg_entry.pack(fill="x", pady=5)
        self.bg_entry.insert(0, getattr(self, 'bg_color', 'white'))
        
        ctk.CTkButton(scroll, text="Apply Custom", command=self.apply_custom_color, fg_color=Colors.BG_MAIN,
                      text_color=Colors.TEXT_MAIN, hover_color=Colors.BG_CARD_HOVER).pack(fill="x", pady=10)
        
        ctk.CTkButton(scroll, text="Reset to Default",  fg_color="transparent", border_width=1, border_color=Colors.BORDER,
                      text_color=Colors.TEXT_MUTED, command=lambda: self.apply_color("black", "white")).pack(fill="x", pady=30)

    def apply_color(self, fg, bg):
        from ..components.dialogs import CustomDialog
        self.fg_color = fg
        self.bg_color = bg
        self.drawer_design.destroy()
        
        if self.vpa_entry.get():
             CustomDialog.show_info(self, "Applied", f"Colors applied: {fg} on {bg}.\nClick Generate to see changes.")
             
    def apply_custom_color(self):
        f = self.fg_entry.get().strip()
        b = self.bg_entry.get().strip()
        if f and b:
            self.apply_color(f, b)

    def save_to_history(self):
        from ..components.dialogs import CustomDialog
        from ...core.history_manager import HistoryManager
        try:
            HistoryManager().add_record(
                self.vpa_entry.get(), self.name_entry.get(), self.amount_entry.get(), self.note_entry.get(),
                "Manual", batch_id=None, paid_status=self.status_var.get(), file_path=None, logo_path=self.logo_path,
                fg_color=getattr(self, 'fg_color', 'black'), bg_color=getattr(self, 'bg_color', 'white')
            )
            CustomDialog.show_info(self, "Success", "Saved to History!")
        except Exception as e:
            CustomDialog.show_error(self, "Error", f"Failed to save history: {e}")

    def download_image(self):
        if not self.preview_image: return
        from ..components.dialogs import CustomDialog
        from ...core.settings_manager import SettingsManager
        
        settings = SettingsManager()
        default_dir = settings.default_save_dir
        initial = default_dir if default_dir and os.path.exists(default_dir) else os.getcwd()
        
        path = filedialog.asksaveasfilename(defaultextension=".png", initialdir=initial,
                                            initialfile=f"UPI_{self.name_entry.get()}_{datetime.now().strftime('%M%S')}.png")
        if path:
            try:
                self.preview_image.save(path)
                CustomDialog.show_info(self, "Saved", f"Image saved to {path}")
            except Exception as e:
                CustomDialog.show_error(self, "Error", str(e))

    def save_as_template(self):
        from ..components.dialogs import CustomDialog
        vpa = self.vpa_entry.get()
        if not vpa:
            CustomDialog.show_error(self, "Validation Error", "Please enter at least a VPA.")
            return
            
        dialog = ctk.CTkInputDialog(text="Enter Template Name (e.g. Monthly Rent):", title="Save Template")
        name = dialog.get_input()
        if name:
            if self.tpl_manager.add_template(name, vpa, self.amount_entry.get(), self.note_entry.get()):
                CustomDialog.show_info(self, "Success", f"Template '{name}' saved!")
            else:
                CustomDialog.show_error(self, "Error", "Failed to save template.")

    def open_template_drawer(self):
        self.drawer = ctk.CTkFrame(self, fg_color=Colors.BG_CARD, width=350)
        self.drawer.place(relx=1, rely=0, relwidth=0.4, relheight=1, anchor="ne")
        self.drawer.lift()
        
        h = ctk.CTkFrame(self.drawer, fg_color="transparent", height=60)
        h.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(h, text="Select Template", font=("Outfit", 20, "bold"), text_color=Colors.TEXT_MAIN).pack(side="left")
        ctk.CTkButton(h, text="✕", width=40, fg_color="transparent", text_color=Colors.TEXT_MAIN,
                      hover_color=Colors.BG_MAIN, command=self.drawer.destroy).pack(side="right")
        
        scroll = ctk.CTkScrollableFrame(self.drawer, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10)
        
        templates = self.tpl_manager.get_templates()
        if not templates:
            ctk.CTkLabel(scroll, text="No templates saved.", text_color=Colors.TEXT_MUTED).pack(pady=50)
            return

        for t in templates:
            card = ctk.CTkFrame(scroll, fg_color=Colors.BG_MAIN, corner_radius=10)
            card.pack(fill="x", pady=5, padx=5)
            
            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(side="left", padx=10, pady=10)
            ctk.CTkLabel(info, text=t['name'], font=("Roboto", 14, "bold"), text_color=Colors.TEXT_MAIN).pack(anchor="w")
            ctk.CTkLabel(info, text=t['vpa'], font=("Roboto", 12), text_color=Colors.TEXT_MUTED).pack(anchor="w")
            
            ctk.CTkButton(card, text="Load", width=60, height=30, fg_color=Colors.PRIMARY, 
                          command=lambda x=t: self.load_template(x)).pack(side="right", padx=10)
            
            ctk.CTkButton(card, text="🗑️", width=30, height=30, fg_color=Colors.ERROR, 
                          command=lambda x=t['id']: self.delete_template_ui(x)).pack(side="right", padx=(0,5))

    def load_template(self, t):
        from ..components.dialogs import CustomDialog
        self.vpa_entry.delete(0, 'end'); self.vpa_entry.insert(0, t['vpa'])
        self.amount_entry.delete(0, 'end'); self.amount_entry.insert(0, t['amount'] if t['amount'] else "")
        self.note_entry.delete(0, 'end'); self.note_entry.insert(0, t['note'] if t['note'] else "")
        self.drawer.destroy()
        CustomDialog.show_info(self, "Loaded", f"Template '{t['name']}' populated.")

    def delete_template_ui(self, tid):
        if self.tpl_manager.delete_template(tid):
            self.drawer.destroy()
            self.open_template_drawer()
            pass
