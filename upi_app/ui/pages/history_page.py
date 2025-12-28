import os
import customtkinter as ctk
from tkinter import messagebox
from ...core.history_manager import HistoryManager
from ...core.qr_generator import UPIQRGenerator
from ..styles import Colors, Fonts, Dims
from ..components.loader import Loader

class HistoryPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.manager = HistoryManager()
        self.items_per_page = 20
        self.current_page = 1
        
        self.loader = Loader(self, width=80, height=80)
        self.loader.place(relx=0.5, rely=0.5, anchor="center")
        self.loader.lower()

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=Dims.PAD_LG, pady=(Dims.PAD_LG, Dims.PAD_MD))
        
        ctk.CTkLabel(self.header_frame, text="History", font=Fonts.HEADER_LG, text_color=Colors.TEXT_MAIN).pack(side="left")
        
        self.controls_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.controls_frame.pack(side="right")
        
        self.filter_status = ctk.StringVar(value="All Status")
        self.filter_source = ctk.StringVar(value="All")
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self.on_search_change)
        
        ctk.CTkEntry(self.controls_frame, textvariable=self.search_var, placeholder_text="Search...", width=200,
                     bg_color="transparent", fg_color=Colors.BG_CARD, text_color=Colors.TEXT_MAIN).pack(side="left", padx=5)
                     
        ctk.CTkOptionMenu(self.controls_frame, variable=self.filter_status, values=["All Status", "Paid", "Unpaid", "Pending"],
                          width=110, fg_color=Colors.BG_CARD, button_color=Colors.PRIMARY, text_color=Colors.TEXT_MAIN, 
                          command=self.on_filter_change).pack(side="left", padx=5)
                          
        self.export_fmt = ctk.StringVar(value="Excel")
        ctk.CTkOptionMenu(self.controls_frame, variable=self.export_fmt, values=["Excel", "PDF"],
                          width=80, fg_color=Colors.BG_CARD, button_color=Colors.PRIMARY, text_color=Colors.TEXT_MAIN).pack(side="left", padx=5)

        ctk.CTkButton(self.controls_frame, text="Export", width=80, fg_color=Colors.SUCCESS, text_color="white",
                      command=self.export_data).pack(side="left", padx=5)
                          
        ctk.CTkButton(self.controls_frame, text="↻", width=40, fg_color=Colors.BG_CARD, text_color=Colors.PRIMARY, 
                      command=self.mount).pack(side="left", padx=5)
        
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True, padx=Dims.PAD_LG, pady=(0, Dims.PAD_MD))
        
        self.list_frame = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        self.list_frame.pack(fill="x", expand=True)

        self.footer = ctk.CTkFrame(self, height=50, fg_color="transparent")
        self.footer.pack(fill="x", padx=20, pady=10)
        self.setup_pagination()

    def setup_pagination(self):
        self.btn_prev = ctk.CTkButton(self.footer, text="< Prev", width=90, height=32, fg_color=Colors.BG_CARD, 
                                      text_color=Colors.TEXT_MAIN, hover_color=Colors.BG_CARD_HOVER, command=self.prev_page)
        self.btn_prev.pack(side="left")
        
        self.lbl_page = ctk.CTkLabel(self.footer, text="Page 1", font=Fonts.BODY_SM, text_color=Colors.TEXT_MUTED)
        self.lbl_page.pack(side="left", padx=20)
        
        self.btn_next = ctk.CTkButton(self.footer, text="Next >", width=90, height=32, fg_color=Colors.BG_CARD, 
                                      text_color=Colors.TEXT_MAIN, hover_color=Colors.BG_CARD_HOVER, command=self.next_page)
        self.btn_next.pack(side="left")

    def mount(self):
        self.loader.lift()
        self.loader.start()
        self.after(100, self.load_data)

    def load_data(self):
        self.all_data = self.manager.get_all()
        self.all_data.sort(key=lambda x: x['timestamp'], reverse=True)
        self.apply_filters()
        self.loader.stop()
        self.loader.lower()

    def on_search_change(self, *args):
        self.current_page = 1
        self.apply_filters()

    def on_filter_change(self, choice):
        self.current_page = 1
        self.apply_filters()

    def apply_filters(self):
        q = self.search_var.get().lower()
        f_stat = self.filter_status.get()
        
        res = []
        for item in self.all_data:
            st = item.get('paid_status') or "Unpaid"
            if f_stat != "All Status" and st != f_stat: continue
            
            if q:
                row_str = f"{item['vpa']} {item['name']} {item.get('note','')} {item.get('amount','')}".lower()
                if q not in row_str: continue
            
            res.append(item)
            
        self.filtered_data = res
        self.render_cards()

    def render_cards(self):
        if not hasattr(self, 'list_frame'): return
        
        for w in self.list_frame.winfo_children(): w.destroy()
        
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        page_items = self.filtered_data[start:end]
        page_items = self.filtered_data[start:end]
        
        total_p = (len(self.filtered_data) + self.items_per_page - 1) // self.items_per_page
        self.lbl_page.configure(text=f"Page {self.current_page} of {max(1, total_p)}")
        self.btn_prev.configure(state="normal" if self.current_page > 1 else "disabled")
        self.btn_next.configure(state="normal" if self.current_page < total_p else "disabled")

        if not page_items:
            ctk.CTkLabel(self.list_frame, text="No records found matching your filters.", font=Fonts.BODY_LG, text_color=Colors.TEXT_MUTED).pack(pady=40)
            return

        for item in page_items:
            self.create_card(item)

    def create_card(self, item):
        card = ctk.CTkFrame(self.list_frame, fg_color=Colors.BG_CARD, corner_radius=12)
        card.pack(fill="x", pady=6, padx=2)
        
        
        left = ctk.CTkFrame(card, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, padx=15, pady=12)
        
        ctk.CTkLabel(left, text=item['name'], font=("Outfit", 16, "bold"), text_color=Colors.TEXT_MAIN, anchor="w").pack(fill="x")
        ctk.CTkLabel(left, text=item['vpa'], font=Fonts.BODY_SM, text_color=Colors.TEXT_MUTED, anchor="w").pack(fill="x")
        if item.get('note'):
             ctk.CTkLabel(left, text=f"📝 {item['note']}", font=("Roboto", 12), text_color=Colors.TEXT_MUTED, anchor="w").pack(fill="x", pady=(2,0))
        
        meta_row = ctk.CTkFrame(left, fg_color="transparent", height=20)
        meta_row.pack(fill="x", pady=(5,0))
        
        dt = item['timestamp'].replace('T', ' ')[:16]
        ctk.CTkLabel(meta_row, text=dt, font=("Roboto", 11), text_color=Colors.TEXT_MUTED).pack(side="left")
        
        src = "Batch" if item.get('batch_id') else "Manual"
        src_col = Colors.PRIMARY if src=="Manual" else "#6b21a8"
        ctk.CTkLabel(meta_row, text=f"• {src}", font=("Roboto", 11, "bold"), text_color=src_col).pack(side="left", padx=8)

        right = ctk.CTkFrame(card, fg_color="transparent")
        right.pack(side="right", padx=15, pady=12)
        
        amt_txt = f"₹{item['amount']}" if item['amount'] else "N/A"
        ctk.CTkLabel(right, text=amt_txt, font=("Outfit", 18, "bold"), text_color=Colors.TEXT_MAIN, anchor="e").pack(anchor="e")
        
        st = item.get('paid_status') or "Unpaid"
        st_col = Colors.SUCCESS if st == "Paid" else Colors.ERROR if st == "Unpaid" else Colors.WARNING
        ctk.CTkLabel(right, text=st, font=("Roboto", 12, "bold"), text_color=st_col, anchor="e").pack(anchor="e", pady=(0, 5))
        
        actions = ctk.CTkFrame(right, fg_color="transparent")
        actions.pack(anchor="e", pady=(5,0))
        
        self.add_icon_btn(actions, "👁", Colors.BG_MAIN, Colors.TEXT_MAIN, lambda: self.view_qr_popup(item))
        self.add_icon_btn(actions, "✏️", Colors.BG_MAIN, Colors.PRIMARY, lambda: self.open_edit_dialog(item))
        self.add_icon_btn(actions, "🗑", Colors.ERROR, "white", lambda: self.delete_item(item['id']))

    def add_icon_btn(self, parent, text, bg, fg, cmd):
        ctk.CTkButton(parent, text=text, width=32, height=32, corner_radius=8,
                      fg_color=bg, text_color=fg, hover_color=Colors.BG_CARD_HOVER,
                      font=("Roboto", 14), command=cmd).pack(side="left", padx=2)

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.render_cards()

    def next_page(self):
        if self.current_page < (len(self.filtered_data) + self.items_per_page - 1) // self.items_per_page:
            self.current_page += 1
            self.render_cards()

    def delete_item(self, rid):
        from ..components.dialogs import CustomDialog
        if CustomDialog.ask_yes_no(self, "Delete", "Permanently delete this record?"):
             self.manager.delete_record(rid)
             self.mount()

    def create_overlay(self):
        self.drawer = ctk.CTkFrame(self, fg_color=Colors.BG_CARD, border_width=0, width=400)
        self.drawer.place(relx=1, rely=0, relwidth=0.35, relheight=1, anchor="ne")
        self.drawer.lift()
        ctk.CTkFrame(self.drawer, width=1, fg_color="gray90").pack(side="left", fill="y")
        return self.drawer

    def close_overlay(self):
        if hasattr(self, 'drawer') and self.drawer.winfo_exists():
            self.drawer.destroy()

    def view_qr_popup(self, item):
        d = self.create_overlay()
        
        h = ctk.CTkFrame(d, fg_color="transparent", height=60)
        h.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(h, text="Details", font=("Outfit", 20, "bold"), text_color=Colors.TEXT_MAIN).pack(side="left")
        ctk.CTkButton(h, text="✕", width=40, height=40, fg_color="transparent", text_color=Colors.TEXT_MAIN, 
                      hover_color=Colors.BG_MAIN, command=self.close_overlay).pack(side="right")
        
        scroll = ctk.CTkScrollableFrame(d, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10)
        
        try:
            gen = UPIQRGenerator()
            fg = item.get('fg_color', 'black')
            bg = item.get('bg_color', 'white')
            pil = gen.generate_qr(item['vpa'], item['name'], item['amount'], item['note'], 
                                logo_path=item.get('logo_path'), fg_color=fg, bg_color=bg)
            c_img = ctk.CTkImage(pil, size=(220, 220))
            ctk.CTkLabel(scroll, image=c_img, text="").pack(pady=20)
        except: pass
        
        self.add_det(scroll, "Payee", item['name'])
        self.add_det(scroll, "VPA", item['vpa'])
        self.add_det(scroll, "Amount", f"₹{item['amount']}" if item['amount'] else "-", True)
        self.add_det(scroll, "Date", item['timestamp'][:16].replace('T',' '))
        self.add_det(scroll, "Status", item.get('paid_status', 'Unpaid'))
        if item.get('batch_id'): self.add_det(scroll, "Batch ID", item['batch_id'])
        
        btn_row = ctk.CTkFrame(scroll, fg_color="transparent")
        btn_row.pack(fill="x", pady=30, padx=20)
        
        ctk.CTkButton(btn_row, text="Print", height=50, width=100, fg_color=Colors.BG_CARD, text_color=Colors.TEXT_MAIN, 
                      font=("Roboto", 14, "bold"), hover_color=Colors.BG_CARD_HOVER, 
                      command=lambda: self.print_qr(pil)).pack(side="left", padx=(0, 5), expand=True, fill="x")

        ctk.CTkButton(btn_row, text="Link", height=50, width=80, fg_color=Colors.INFO, text_color="white",
                      font=("Roboto", 14, "bold"), hover_color="#2897c2",
                      command=lambda: self.copy_link_history(item)).pack(side="left", padx=(0, 5), expand=True, fill="x")

        ctk.CTkButton(btn_row, text="Download", height=50, width=100, fg_color=Colors.PRIMARY, hover_color=Colors.PRIMARY_HOVER, 
                      font=("Roboto", 14, "bold"), command=lambda: self.download_qr_from_history(pil, item)).pack(side="left", expand=True, fill="x")

    def add_det(self, p, lbl, val, bold=False):
        f = ctk.CTkFrame(p, fg_color="transparent")
        f.pack(fill="x", pady=8, padx=10)
        ctk.CTkLabel(f, text=lbl, font=Fonts.BODY_SM, text_color=Colors.TEXT_MUTED).pack(anchor="w")
        font = ("Outfit", 16, "bold") if bold else ("Roboto", 14)
        ctk.CTkLabel(f, text=val, font=font, text_color=Colors.TEXT_MAIN).pack(anchor="w")

    def open_edit_dialog(self, item):
        d = self.create_overlay()
        h = ctk.CTkFrame(d, fg_color="transparent", height=60)
        h.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(h, text="Edit Record", font=Fonts.HEADER_LG, text_color=Colors.TEXT_MAIN).pack(side="left")
        ctk.CTkButton(h, text="✕", width=40, fg_color="transparent", command=self.close_overlay).pack(side="right")
        
        c = ctk.CTkScrollableFrame(d, fg_color="transparent")
        c.pack(fill="both", expand=True, padx=20)
        
        vars = {
            'vpa': ctk.StringVar(value=item['vpa']),
            'name': ctk.StringVar(value=item['name']),
            'amt': ctk.StringVar(value=item['amount']),
            'note': ctk.StringVar(value=item['note']),
            'status': ctk.StringVar(value=item.get('paid_status','Unpaid')),
            'logo': item.get('logo_path'),
            'fg_color': item.get('fg_color', 'black'),
            'bg_color': item.get('bg_color', 'white')
        }
        
        self.mk_inp(c, "VPA", vars['vpa'])
        self.mk_inp(c, "Name", vars['name'])
        self.mk_inp(c, "Amount", vars['amt'])
        self.mk_inp(c, "Note", vars['note'])
        
        ctk.CTkLabel(c, text="Logo", font=Fonts.BODY_SM, text_color=Colors.TEXT_MUTED).pack(anchor="w", pady=(10,5))
        logo_frame = ctk.CTkFrame(c, fg_color=Colors.BG_MAIN, height=40)
        logo_frame.pack(fill="x")
        
        logo_lbl = ctk.CTkLabel(logo_frame, text=os.path.basename(vars['logo']) if vars['logo'] else "No Logo", text_color=Colors.TEXT_MAIN)
        logo_lbl.pack(side="left", padx=10)
        
        def pick_logo():
            from tkinter import filedialog
            path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
            if path:
                vars['logo'] = path
                logo_lbl.configure(text=os.path.basename(path))

        ctk.CTkButton(logo_frame, text="Change", width=60, command=pick_logo, fg_color=Colors.BG_CARD, text_color=Colors.TEXT_MAIN).pack(side="right", padx=5, pady=5)

        ctk.CTkLabel(c, text="Status", font=Fonts.BODY_SM, text_color=Colors.TEXT_MUTED).pack(anchor="w", pady=(10,5))
        ctk.CTkOptionMenu(c, variable=vars['status'], values=["Paid","Unpaid","Pending"], fg_color=Colors.BG_MAIN, button_color=Colors.PRIMARY).pack(fill="x")
        
        ctk.CTkLabel(c, text="QR Design", font=Fonts.BODY_SM, text_color=Colors.TEXT_MUTED).pack(anchor="w", pady=(15,5))
        
        color_frame = ctk.CTkFrame(c, fg_color=Colors.BG_MAIN, height=60, corner_radius=8)
        color_frame.pack(fill="x", pady=(0, 5))
        
        ctk.CTkLabel(color_frame, text="FG:", font=Fonts.BODY_SM, text_color=Colors.TEXT_MAIN).pack(side="left", padx=(10, 5))
        fg_entry = ctk.CTkEntry(color_frame, width=100, height=30)
        fg_entry.insert(0, vars['fg_color'])
        fg_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(color_frame, text="BG:", font=Fonts.BODY_SM, text_color=Colors.TEXT_MAIN).pack(side="left", padx=(15, 5))
        bg_entry = ctk.CTkEntry(color_frame, width=100, height=30)
        bg_entry.insert(0, vars['bg_color'])
        bg_entry.pack(side="left", padx=5)
        
        def apply_color():
            vars['fg_color'] = fg_entry.get().strip()
            vars['bg_color'] = bg_entry.get().strip()
        
        ctk.CTkButton(color_frame, text="Apply", width=60, height=30, command=apply_color, fg_color=Colors.PRIMARY, text_color="white").pack(side="right", padx=10)
        
        def save():
            from ..components.dialogs import CustomDialog
            final_logo_path = item.get('logo_path')
            
            if vars['logo'] != item.get('logo_path'):
                 if vars['logo']:
                      import shutil
                      media_dir = os.path.join(os.getcwd(), "media")
                      os.makedirs(media_dir, exist_ok=True)
                      
                      ext = os.path.splitext(vars['logo'])[1]
                      new_filename = f"logo_{item['id']}{ext}"
                      dest_path = os.path.join(media_dir, new_filename)
                      
                      try:
                          shutil.copy2(vars['logo'], dest_path)
                          final_logo_path = dest_path
                          
                      except Exception as e:
                          CustomDialog.show_error(self, "Error", f"Failed to save logo: {e}")
                          return
                 else:
                     final_logo_path = None

            self.manager.update_record(item['id'], vars['vpa'].get(), vars['name'].get(), vars['amt'].get(), vars['note'].get(), vars['status'].get(), 
                                      logo_path=final_logo_path, fg_color=vars['fg_color'], bg_color=vars['bg_color'])
            self.mount()
            self.close_overlay()
            
        ctk.CTkButton(c, text="Save Changes", height=50, fg_color=Colors.SUCCESS, hover_color="#00a844", font=("Roboto", 14, "bold"), command=save).pack(fill="x", pady=40)

    def mk_inp(self, p, l, v):
        ctk.CTkLabel(p, text=l, font=Fonts.BODY_SM, text_color=Colors.TEXT_MUTED).pack(anchor="w", pady=(10,5))
        ctk.CTkEntry(p, textvariable=v, height=45, border_color=Colors.BORDER, fg_color=Colors.BG_MAIN, text_color=Colors.TEXT_MAIN).pack(fill="x")
        
    def download_qr_from_history(self, pil_img, item):
        from ...core.settings_manager import SettingsManager
        from tkinter import filedialog
        import os
        settings = SettingsManager()
        default_dir = settings.default_save_dir
        initial = default_dir if default_dir and os.path.exists(default_dir) else os.getcwd()
        path = filedialog.asksaveasfilename(defaultextension=".png", initialdir=initial, initialfile=f"UPI_{item['name']}.png")
        if path:
             try: 
                 pil_img.save(path)
                 from ..components.dialogs import CustomDialog
                 CustomDialog.show_info(self, "Saved", path)
             except Exception as e: 
                 from ..components.dialogs import CustomDialog
                 CustomDialog.show_error(self, "Error", str(e))

    def export_data(self):
        from tkinter import filedialog
        import pandas as pd
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from datetime import datetime
        
        data = self.filtered_data if self.filtered_data else self.all_data
        if not data:
            from ..components.dialogs import CustomDialog
            CustomDialog.show_error(self, "Export", "No data to export.")
            return

        fmt = self.export_fmt.get()
        if fmt == "Excel":
            ext, ft = ".xlsx", [("Excel File", "*.xlsx")]
        else:
            ext, ft = ".pdf", [("PDF Document", "*.pdf")]

        filename = filedialog.asksaveasfilename(
            defaultextension=ext,
            filetypes=ft,
            title=f"Export History as {fmt}"
        )
        
        if not filename: return
        
        try:
            self.loader.lift(); self.loader.start()
            
            df = pd.DataFrame(data)
            cols = ['timestamp', 'vpa', 'name', 'amount', 'paid_status', 'source', 'note']
            df = df[[c for c in cols if c in df.columns]]
            
            if filename.endswith(".xlsx"):
                df.to_excel(filename, index=False)
                
            elif filename.endswith(".pdf"):
                c = canvas.Canvas(filename, pagesize=letter)
                width, height = letter
                y = height - 50
                
                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, y, "QRMint History Report")
                y -= 30
                c.setFont("Helvetica", 10)
                c.drawString(50, y, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                y -= 30
                
                headers = ["Time", "Name", "VPA", "Amount", "Status"]
                x_offsets = [50, 150, 250, 400, 480]
                
                c.setFont("Helvetica-Bold", 10)
                for i, h in enumerate(headers):
                    c.drawString(x_offsets[i], y, h)
                
                y -= 20
                c.setFont("Helvetica", 9)
                
                for item in data:
                    if y < 50:
                        c.showPage()
                        y = height - 50
                    
                    row = [
                        item.get('timestamp','').replace('T',' ')[:16],
                        item.get('name','')[:15],
                        item.get('vpa','')[:20],
                        f"Rs. {item.get('amount','')}",
                        item.get('paid_status','Unpaid')
                    ]
                    
                    for i, r in enumerate(row):
                         c.drawString(x_offsets[i], y, str(r))
                    y -= 15
                    
                c.save()
                
            from ..components.dialogs import CustomDialog
            CustomDialog.show_info(self, "Success", f"Data exported successfully to:\n{filename}")
            
        except Exception as e:
            from ..components.dialogs import CustomDialog
            CustomDialog.show_error(self, "Export Failed", str(e))
        finally:
            self.loader.stop(); self.loader.lower()

    def print_qr(self, pil_img):
        import tempfile
        try:
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                pil_img.save(tmp.name)
                tmp_path = tmp.name
            
            if os.name == 'nt':
                os.startfile(tmp_path, "print")
            else:
                 from ..components.dialogs import CustomDialog
                 CustomDialog.show_info(self, "Print", "Printing is only supported on Windows for now.\nFile saved at: " + tmp_path)
                
        except Exception as e:
            from ..components.dialogs import CustomDialog
            CustomDialog.show_error(self, "Print Error", str(e))
            
    def copy_link_history(self, item):
        try:
             gen = UPIQRGenerator()
             link = gen.generate_upi_link(item['vpa'], item['name'], item['amount'], item['note'])
             
             self.clipboard_clear()
             self.clipboard_append(link)
             self.update()
             
             from ..components.dialogs import CustomDialog
             CustomDialog.show_info(self, "Copied", "Payment link copied to clipboard!")
        except Exception as e:
             from ..components.dialogs import CustomDialog
             CustomDialog.show_error(self, "Error", str(e))
