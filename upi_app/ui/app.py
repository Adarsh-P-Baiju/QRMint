import customtkinter as ctk
from .styles import Colors, Dims
from .components.sidebar import Sidebar
from .pages.dashboard_page import DashboardPage
from .pages.generator_page import GeneratorPage
from .pages.batch_page import BatchPage
from .pages.history_page import HistoryPage
from .pages.templates_page import TemplatesPage
from .pages.banks_page import BanksPage
from .pages.settings_page import SettingsPage
from .pages.login_page import LoginPage
from ..core.auth_manager import AuthManager

class UPIApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        self.resizable(False, False)
        
       
        self.title("QRMint - UPI QR Code Generator")
        

        try:
            import ctypes
            myappid = 'qrmint.upi.qrcodegenerator.1.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except:
            pass
        

        try:
            import os
            icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Could not load icon: {e}")
        

        self.bind("<Escape>", self.confirm_exit)
        self.bind("<Control-c>", self.confirm_exit)
        
        ctk.set_appearance_mode("Light")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.auth = AuthManager()
        self.check_auth()

    def check_auth(self):

        if True:
             self.login_ui = LoginPage(self, self.load_main_app, self)
             self.login_ui.grid(row=0, column=0, sticky="nsew")
             
    def load_main_app(self):

        if hasattr(self, 'login_ui'):
            self.login_ui.destroy()
            

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        

        self.sidebar = Sidebar(self, self.navigate, self)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        

        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color=Colors.BG_MAIN)
        self.main_container.grid(row=0, column=1, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        

        self.pages = {}
        self.current_page = None
        

        self.register_page("dashboard", DashboardPage)
        self.register_page("generator", GeneratorPage)
        self.register_page("templates", TemplatesPage)
        self.register_page("batch", BatchPage)
        self.register_page("history", HistoryPage)
        self.register_page("banks", BanksPage)
        self.register_page("settings", SettingsPage)
        

        self.navigate("dashboard")
        
    def register_page(self, name, page_class):
         self.pages[name] = page_class(self.main_container)
         
    def navigate(self, page_name):
        if page_name in self.pages:

            if self.current_page:
                self.current_page.grid_forget()
            

            self.current_page = self.pages[page_name]
            self.current_page.grid(row=0, column=0, sticky="nsew")
            

            if hasattr(self.sidebar, 'update_active_state'):
                 self.sidebar.update_active_state(page_name)
            

            if hasattr(self.current_page, 'mount'):
                self.current_page.mount()


        self.bind("<Configure>", self.on_resize)
        self.last_width = 1200

    def on_resize(self, event):
        if event.widget != self: return
        

        if abs(event.width - self.last_width) < 50: return
        self.last_width = event.width
        

        if event.width < 900 and not self.sidebar.is_collapsed:
            self.sidebar.toggle_collapse()
        elif event.width >= 900 and self.sidebar.is_collapsed:
             self.sidebar.toggle_collapse()

    def confirm_exit(self, event=None):
        from .components.dialogs import CustomDialog
        if CustomDialog.ask_yes_no(self, "Exit QRMint", "Are you sure you want to quit?"):
            self.quit()

    def run(self):
        self.mainloop()
