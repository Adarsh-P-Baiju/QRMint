import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ...core.history_manager import HistoryManager
from ...core.analytics_manager import AnalyticsManager
from ..styles import Colors, Fonts, Dims
from ..components.loader import Loader
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DashboardPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        self.loader = Loader(self, width=60, height=60)
        self.loader.place(relx=0.5, rely=0.5, anchor="center")
        self.loader.lower()
        
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True)
        
        self.content = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.content.pack(fill="x", padx=Dims.PAD_LG, pady=Dims.PAD_LG)
        
        self.header = ctk.CTkFrame(self.content, fg_color="transparent")
        self.header.pack(fill="x", pady=(0, Dims.PAD_MD))
        
        ctk.CTkLabel(self.header, text="Dashboard Overview", font=("Roboto", 28, "bold"), text_color=Colors.TEXT_MAIN).pack(side="left")
        
        self.refresh_btn = ctk.CTkButton(self.header, text="Refresh Data", width=120, height=40,
                                       fg_color=Colors.BG_CARD, hover_color=Colors.BG_CARD_HOVER,
                                       text_color=Colors.PRIMARY, font=Fonts.BODY_MD,
                                       command=self.mount)
        self.refresh_btn.pack(side="right")
        
        self.kpi_container = ctk.CTkFrame(self.content, fg_color="transparent")
        self.kpi_container.pack(fill="x", pady=(0, Dims.PAD_LG))
        self.kpi_container.grid_columnconfigure((0, 1, 2), weight=1, uniform="kpi")
        
        self.card_total = self.create_kpi_card(self.kpi_container, 0, "Total Generated", "₹0.00", "📦", Colors.PRIMARY)
        self.card_paid = self.create_kpi_card(self.kpi_container, 1, "Total Paid", "₹0.00", "✅", Colors.SUCCESS)
        self.card_unpaid = self.create_kpi_card(self.kpi_container, 2, "Unpaid / Pending", "₹0.00", "⚠️", Colors.WARNING)
        
        self.charts_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        self.charts_frame.pack(fill="x", pady=(0, Dims.PAD_LG))
        self.charts_frame.grid_columnconfigure(0, weight=2)
        self.charts_frame.grid_columnconfigure(1, weight=1)
        
        self.chart_container = ctk.CTkFrame(self.charts_frame, fg_color="transparent")
        self.chart_container.pack(fill="both", expand=True)
        
        ctk.CTkLabel(self.content, text="Recent Transactions", font=Fonts.HEADER_MD, text_color=Colors.TEXT_MAIN).pack(anchor="w", pady=(10, 10))
        self.recent_frame = ctk.CTkFrame(self.content, fg_color=Colors.BG_CARD, corner_radius=Dims.CORNER_RADIUS)
        self.recent_frame.pack(fill="x")

    def create_kpi_card(self, parent, col_idx, title, value, icon, color):
        card = ctk.CTkFrame(parent, fg_color=Colors.BG_CARD, corner_radius=Dims.CORNER_RADIUS, height=120)
        card.grid(row=0, column=col_idx, padx=10, sticky="ew")
        card.pack_propagate(False)
        
        icon_box = ctk.CTkFrame(card, width=50, height=50, corner_radius=12, fg_color=color)
        icon_box.pack(side="left", padx=20)
        ctk.CTkLabel(icon_box, text=icon, font=("Roboto", 24), text_color="white").place(relx=0.5, rely=0.5, anchor="center")
        
        info_box = ctk.CTkFrame(card, fg_color="transparent")
        info_box.pack(side="left", pady=25)
        
        lbl_val = ctk.CTkLabel(info_box, text=value, font=("Roboto", 22, "bold"), text_color=Colors.TEXT_MAIN)
        lbl_val.pack(anchor="w")
        
        ctk.CTkLabel(info_box, text=title, font=Fonts.BODY_SM, text_color=Colors.TEXT_MUTED).pack(anchor="w")
        
        return lbl_val

    def mount(self):
        self.loader.lift()
        self.manager = HistoryManager()
        self.analytics = AnalyticsManager()
        self.loader.start()
        
        self.after(600, self.load_data)

    def load_data(self):
        stats = self.analytics.get_status_counts()
        total = sum(stats.values())
        paid = stats.get('Paid', 0)
        unpaid = stats.get('Unpaid', 0)
        
        for w in self.chart_container.winfo_children(): w.destroy()
        
        pie_card = ctk.CTkFrame(self.chart_container, fg_color=Colors.BG_CARD, corner_radius=16)
        pie_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        
        ctk.CTkLabel(pie_card, text="Payment Status", font=Fonts.HEADER_SM, text_color=Colors.TEXT_MAIN).pack(pady=10)
        
        if total > 0:
            fig1 = plt.Figure(figsize=(4, 3), dpi=100, facecolor="#ffffff") 
            ax1 = fig1.add_subplot(111)
            
            labels = [k for k,v in stats.items() if v > 0]
            sizes = [v for k,v in stats.items() if v > 0]
            colors_map = {"Paid": "#2ecc71", "Unpaid": "#e74c3c", "Pending": "#f1c40f"}
            cols = [colors_map.get(l, "#95a5a6") for l in labels]
            
            wedges, _ = ax1.pie(sizes, colors=cols, startangle=90)
            ax1.legend(wedges, labels, loc="center left", bbox_to_anchor=(0.9, 0, 0.5, 1))
            ax1.set_title(f"Total: {total}", fontsize=10)
            
            canvas1 = FigureCanvasTkAgg(fig1, pie_card)
            canvas1.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        else:
            ctk.CTkLabel(pie_card, text="No Data Available", text_color=Colors.TEXT_MUTED).pack(expand=True)

        bar_card = ctk.CTkFrame(self.chart_container, fg_color=Colors.BG_CARD, corner_radius=16)
        bar_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)
        
        ctk.CTkLabel(bar_card, text="Last 7 Days Activity", font=Fonts.HEADER_SM, text_color=Colors.TEXT_MAIN).pack(pady=10)
        
        dates, counts = self.analytics.get_daily_trend()
        
        if any(counts):
            fig2 = plt.Figure(figsize=(5, 3), dpi=100, facecolor="#ffffff")
            ax2 = fig2.add_subplot(111)
            
            ax2.bar(dates, counts, color=Colors.PRIMARY)
            ax2.set_ylabel("QRs Generated")
            ax2.tick_params(axis='x', rotation=45, labelsize=8)
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            
            fig2.tight_layout()
            
            canvas2 = FigureCanvasTkAgg(fig2, bar_card)
            canvas2.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        else:
             ctk.CTkLabel(bar_card, text="No Activity Recently", text_color=Colors.TEXT_MUTED).pack(expand=True)
             
        self.perform_kpi_updates(paid, unpaid)
        
        recent = self.analytics.get_recent_history()
        self.render_recent(recent)

        self.loader.stop()
        self.loader.lower()

    def perform_kpi_updates(self, paid_cnt, unpaid_cnt):
         self.card_total.configure(text=f"{paid_cnt + unpaid_cnt}")
         self.card_paid.configure(text=f"{paid_cnt}")
         self.card_unpaid.configure(text=f"{unpaid_cnt}")

    def render_recent(self, history):
        for widget in self.recent_frame.winfo_children():
            widget.destroy()
            
        if not history:
            ctk.CTkLabel(self.recent_frame, text="No recent activity", font=Fonts.BODY_SM, text_color=Colors.TEXT_MUTED).pack(pady=20)
            return
            
        head = ctk.CTkFrame(self.recent_frame, fg_color="transparent", height=40)
        head.pack(fill="x", padx=20, pady=10)
        self.add_col(head, "Date", 120, is_head=True)
        self.add_col(head, "Name", 200, is_head=True)
        self.add_col(head, "Amount", 100, is_head=True)
        self.add_col(head, "Status", 100, is_head=True)
        
        ctk.CTkFrame(self.recent_frame, height=1, fg_color=Colors.BORDER).pack(fill="x")
        
        for item in history:
            row = ctk.CTkFrame(self.recent_frame, fg_color="transparent", height=50)
            row.pack(fill="x", padx=20, pady=5)
            
            self.add_col(row, item['timestamp'][:10], 120)
            self.add_col(row, item['name'], 200)
            self.add_col(row, f"₹{item['amount']}" if item['amount'] else "-", 100)
            
            st = item.get('paid_status', 'Unpaid')
            col = Colors.SUCCESS if st == "Paid" else Colors.WARNING
            badge = ctk.CTkLabel(row, text=st, font=("Roboto", 11, "bold"), text_color=col, width=80) 
            badge.pack(side="left", padx=5)

    def add_col(self, parent, text, w, is_head=False):
        font = ("Roboto", 12, "bold") if is_head else ("Roboto", 12)
        color = Colors.TEXT_MUTED if is_head else Colors.TEXT_MAIN
        ctk.CTkLabel(parent, text=text, font=font, text_color=color, width=w, anchor="w").pack(side="left", padx=5)
