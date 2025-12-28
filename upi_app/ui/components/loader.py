import customtkinter as ctk
import math
from ..styles import Colors

class Loader(ctk.CTkFrame):
    def __init__(self, master, width=100, height=100):
        super().__init__(master, width=width, height=height, fg_color="transparent")
        self.canvas = ctk.CTkCanvas(self, width=width, height=height, bg=Colors.BG_MAIN, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.width = width
        self.height = height
        self.angle = 0
        self.is_running = False
        self.arc_ids = []
        
        self.cx = width / 2
        self.cy = height / 2
        self.radius = min(width, height) / 3
        self.width_pen = 6

        self.draw_static_ring()

    def draw_static_ring(self):
        self.canvas.create_oval(
            self.cx - self.radius, self.cy - self.radius,
            self.cx + self.radius, self.cy + self.radius,
            outline=Colors.BORDER, width=self.width_pen
        )

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.animate()
            
    def stop(self):
        self.is_running = False
        for arc in self.arc_ids:
            self.canvas.delete(arc)
        self.arc_ids = []

    def animate(self):
        if not self.is_running:
            return
            
        for arc in self.arc_ids:
            self.canvas.delete(arc)
        self.arc_ids = []
        
        
        start = self.angle
        extent = 120
        
        arc = self.canvas.create_arc(
            self.cx - self.radius, self.cy - self.radius,
            self.cx + self.radius, self.cy + self.radius,
            start=start, extent=extent, style="arc",
            outline=Colors.PRIMARY, width=self.width_pen
        )
        self.arc_ids.append(arc)
        
        self.angle = (self.angle - 10) % 360
        
        self.after(20, self.animate)
