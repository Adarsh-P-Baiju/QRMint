import customtkinter as ctk
from tkinter import messagebox
from ...core.template_manager import TemplateManager
from ..styles import Colors, Fonts, Dims
from ..components.loader import Loader

class TemplatesPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.manager = TemplateManager()
        
        self.loader = Loader(self, width=60, height=60)
        self.loader.place(relx=0.5, rely=0.5, anchor="center")
        self.loader.lower()
        
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=Dims.PAD_LG, pady=Dims.PAD_LG)
        
        ctk.CTkLabel(self.header, text="Recurring Templates", font=("Roboto", 28, "bold"), text_color=Colors.TEXT_MAIN).pack(side="left")
        
        ctk.CTkButton(self.header, text="+ Add New", width=120, height=40, font=Fonts.BODY_MD,
                      fg_color=Colors.PRIMARY, hover_color=Colors.PRIMARY_HOVER,
                      command=self.open_add_dialog).pack(side="right")

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=Dims.PAD_LG, pady=(0, Dims.PAD_LG))

    def mount(self):
        self.render_list()

    def render_list(self):
        for w in self.scroll.winfo_children(): w.destroy()
        
        templates = self.manager.get_templates()
        if not templates:
            ctk.CTkLabel(self.scroll, text="No templates found", font=Fonts.BODY_MD, text_color=Colors.TEXT_MUTED).pack(pady=40)
            return
            
        for t in templates:
            card = ctk.CTkFrame(self.scroll, fg_color=Colors.BG_CARD, corner_radius=12)
            card.pack(fill="x", pady=8)
            
            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(side="left", padx=20, pady=20)
            
            ctk.CTkLabel(info, text=t['name'], font=("Roboto", 18, "bold"), text_color=Colors.TEXT_MAIN).pack(anchor="w")
            sub = f"{t['vpa']} • ₹{t['amount'] or '0'} • {t['note'] or 'No Note'}"
            ctk.CTkLabel(info, text=sub, font=Fonts.BODY_SM, text_color=Colors.TEXT_MUTED).pack(anchor="w")
            
            actions = ctk.CTkFrame(card, fg_color="transparent")
            actions.pack(side="right", padx=20)
            
            ctk.CTkButton(actions, text="🗑️", width=40, height=40, fg_color=Colors.BG_MAIN, hover_color=Colors.ERROR,
                          text_color=Colors.TEXT_MAIN, command=lambda x=t['id']: self.delete_t(x)).pack(side="right")

    def delete_t(self, tid):
        from ..components.dialogs import CustomDialog
        if CustomDialog.ask_yes_no(self, "Delete", "Are you sure?"):
            self.manager.delete_template(tid)
            self.render_list()

    def open_add_dialog(self):
        self.drawer = ctk.CTkFrame(self, fg_color=Colors.BG_CARD, width=400)
        self.drawer.place(relx=1, rely=0, relwidth=0.4, relheight=1, anchor="ne")
        self.drawer.lift()
        
        ctk.CTkFrame(self.drawer, width=1, fg_color="gray90").pack(side="left", fill="y")
        
        h = ctk.CTkFrame(self.drawer, fg_color="transparent", height=60)
        h.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(h, text="New Template", font=("Outfit", 20, "bold"), text_color=Colors.TEXT_MAIN).pack(side="left")
        ctk.CTkButton(h, text="✕", width=40, fg_color="transparent", command=self.drawer.destroy).pack(side="right")
        
        f = ctk.CTkScrollableFrame(self.drawer, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=20)
        
        self.t_name = self.mk_inp(f, "Template Name *", "Monthly Rent")
        self.t_vpa = self.mk_inp(f, "VPA *", "merchant@upi")
        self.t_amt = self.mk_inp(f, "Amount", "1000")
        self.t_note = self.mk_inp(f, "Note", "Bill Payment")
        
        ctk.CTkButton(f, text="Save Template", height=45, fg_color=Colors.PRIMARY, 
                      font=("Roboto", 14, "bold"), command=self.save_new).pack(fill="x", pady=30)
                      
    def mk_inp(self, p, lbl, ph):
        ctk.CTkLabel(p, text=lbl, font=Fonts.BODY_SM, text_color=Colors.TEXT_MUTED).pack(anchor="w", pady=(10,5))
        e = ctk.CTkEntry(p, height=40, placeholder_text=ph)
        e.pack(fill="x")
        return e
        
    def save_new(self):
        from ..components.dialogs import CustomDialog
        name = self.t_name.get()
        vpa = self.t_vpa.get()
        
        if not name or not vpa:
            CustomDialog.show_error(self, "Error", "Name and VPA form fields are required.")
            return
            
        if self.manager.add_template(name, vpa, self.t_amt.get(), self.t_note.get()):
            CustomDialog.show_info(self, "Success", "Template Saved!")
            self.drawer.destroy()
            self.render_list()
        else:
            CustomDialog.show_error(self, "Error", "Failed to save.")
