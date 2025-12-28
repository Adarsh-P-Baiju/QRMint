import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
from datetime import datetime
import os
import openpyxl
from ...core.excel_handler import generate_batch_excel_workbook
from ...core.history_manager import HistoryManager
from ..styles import Fonts, Colors, Dims
from ..components.loader import Loader

class BatchPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        self.loader = Loader(self, width=80, height=80)
        self.loader.place(relx=0.5, rely=0.5, anchor="center")
        self.loader.lower()

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True)
        
        self.container = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.container.pack(expand=True, fill="both", padx=Dims.PAD_LG, pady=Dims.PAD_LG)
        
        self.header_card = ctk.CTkFrame(self.container, fg_color=Colors.BG_CARD, corner_radius=Dims.CORNER_RADIUS)
        self.header_card.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(self.header_card, text="Batch Processing", font=Fonts.HEADER_LG, text_color=Colors.TEXT_MAIN).pack(anchor="w", padx=20, pady=(20, 5))
        ctk.CTkLabel(self.header_card, text="Generate multiple QRs at once using Excel or CSV. Required columns: vpa, name", 
                     font=Fonts.BODY_MD, text_color=Colors.TEXT_MUTED).pack(anchor="w", padx=20, pady=(0, 20))

        self.upload_card = ctk.CTkFrame(self.container, fg_color=Colors.BG_CARD, corner_radius=Dims.CORNER_RADIUS)
        self.upload_card.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(self.upload_card, text="1. Upload Data Source", font=Fonts.HEADER_SM, text_color=Colors.TEXT_MAIN).pack(anchor="w", padx=20, pady=(20, 10))
        
        self.drop_area = ctk.CTkFrame(self.upload_card, fg_color=Colors.BG_MAIN, height=150, border_color=Colors.PRIMARY, border_width=2, corner_radius=12)
        self.drop_area.pack(fill="x", padx=20, pady=(0, 20))
        self.drop_area.pack_propagate(False)
        
        self.lbl_icon = ctk.CTkLabel(self.drop_area, text="📂", font=("Roboto", 40))
        self.lbl_icon.place(relx=0.5, rely=0.35, anchor="center")
        
        self.lbl_file = ctk.CTkLabel(self.drop_area, text="No file selected", font=Fonts.BODY_MD, text_color=Colors.TEXT_MUTED)
        self.lbl_file.place(relx=0.5, rely=0.6, anchor="center")
        
        ctk.CTkButton(self.drop_area, text="Browse File (Excel/CSV)", command=self.browse_file, height=36,
                      fg_color=Colors.PRIMARY, hover_color=Colors.PRIMARY_HOVER).place(relx=0.5, rely=0.8, anchor="center")
                      
        ctk.CTkButton(self.upload_card, text="Download Sample Template", command=self.download_template, 
                      fg_color="transparent", text_color=Colors.PRIMARY, hover=False, 
                      font=Fonts.BODY_SM).pack(anchor="e", padx=20, pady=(0, 10))

        self.opts_card = ctk.CTkFrame(self.container, fg_color=Colors.BG_CARD, corner_radius=Dims.CORNER_RADIUS)
        self.opts_card.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(self.opts_card, text="2. Process Options", font=Fonts.HEADER_SM, text_color=Colors.TEXT_MAIN).pack(anchor="w", padx=20, pady=(20, 10))
        
        self.download_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(self.opts_card, text="Generate & Download Excel Report", variable=self.download_var, 
                        font=Fonts.BODY_MD, text_color=Colors.TEXT_MAIN, fg_color=Colors.PRIMARY).pack(anchor="w", padx=20, pady=(0, 10))
                        
        self.filename_entry = ctk.CTkEntry(self.opts_card, placeholder_text="Custom Filename (Optional)", width=300, 
                                           border_color=Colors.BORDER, fg_color=Colors.BG_MAIN, text_color=Colors.TEXT_MAIN)
        self.filename_entry.pack(anchor="w", padx=20, pady=(0, 20))
        
        self.btn_process = ctk.CTkButton(self.container, text="START BATCH PROCESS", 
                                       command=self.run_batch, 
                                       height=55, font=("Roboto", 16, "bold"),
                                       fg_color=Colors.SUCCESS, hover_color=Colors.SUCCESS,
                                       state="disabled")
        self.btn_process.pack(fill="x", pady=(0, 10))
        
        self.status_lbl = ctk.CTkLabel(self.container, text="Ready", text_color=Colors.TEXT_MUTED, font=Fonts.BODY_SM)
        self.status_lbl.pack()
        
        self.file_path = None

    def download_template(self):
        filename = filedialog.asksaveasfilename(initialfile="UPI_Batch_Template.xlsx", defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if filename:
            from ..components.dialogs import CustomDialog
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(["vpa", "name", "amount", "note", "status"])
            ws.append(["example@upi", "John Doe", "100", "Services", "Unpaid"])
            wb.save(filename)
            CustomDialog.show_info(self, "Success", f"Template saved to:\n{filename}")
        
    def browse_file(self):
        path = filedialog.askopenfilename(filetypes=[("Data Files", "*.xlsx;*.xls;*.csv")])
        if path:
            self.file_path = path
            self.lbl_file.configure(text=f"Selected: {os.path.basename(path)}", text_color=Colors.TEXT_MAIN)
            self.lbl_icon.configure(text="✅")
            self.btn_process.configure(state="normal", fg_color=Colors.SUCCESS)
            
    def run_batch(self):
        self.loader.lift()
        self.loader.start()
        self.btn_process.configure(state="disabled")
        self.status_lbl.configure(text="Processing...", text_color=Colors.PRIMARY)
        self.after(500, self._process_logic)
        
    def _process_logic(self):
        from ...core.settings_manager import SettingsManager
        from ..components.dialogs import CustomDialog
        try:
            settings = SettingsManager()
            
            if self.file_path.lower().endswith('.csv'):
                df = pd.read_csv(self.file_path)
            else:
                df = pd.read_excel(self.file_path)
                
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
            
            df.columns = [c.lower().strip() for c in df.columns]
            if 'vpa' not in df.columns: raise ValueError("Missing 'vpa' column.")
            
            hm = HistoryManager()
            for _, row in df.iterrows():
                hm.add_record(
                    vpa=str(row['vpa']),
                    name=str(row.get('name', '')),
                    amount=str(row.get('amount', '')),
                    note=str(row.get('note', '')),
                    source="Batch",
                    batch_id=timestamp,
                    paid_status=str(row.get('status', 'Unpaid')),
                    file_path=None
                )
            
            msg = "Batch processed to History."
            if self.download_var.get():
                wb = generate_batch_excel_workbook(df)
                s_dir = settings.default_save_dir
                fname = self.filename_entry.get().strip() or f"Batch_{timestamp}.xlsx"
                if not fname.endswith(".xlsx"): fname += ".xlsx"
                
                if s_dir and os.path.exists(s_dir):
                    path = os.path.join(s_dir, fname)
                else:
                    path = filedialog.asksaveasfilename(initialfile=fname, defaultextension=".xlsx")
                    
                if path:
                    wb.save(path)
                    msg += f"\nReport: {os.path.basename(path)}"
            
            self.status_lbl.configure(text="Completed!", text_color=Colors.SUCCESS)
            CustomDialog.show_info(self, "Success", msg)
            
        except Exception as e:
            self.status_lbl.configure(text="Failed", text_color=Colors.ERROR)
            CustomDialog.show_error(self, "Error", str(e))
        finally:
            self.loader.stop()
            self.loader.lower()
            self.btn_process.configure(state="normal")
