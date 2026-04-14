import tkinter as tk
from tkinter import ttk
from gui.mode1_panel import Mode1Panel
from gui.mode2_panel import Mode2Panel
from mode1.camera import Camera
from mode1.tts_engine import TTSEngine

class SilentBridgeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SilentBridge — Bi-Directional Communication")
        self.root.geometry("1200x700")
        self.root.minsize(900, 550)
        
        self.camera = Camera()
        self.tts_engine = TTSEngine()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Top bar
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        self.mode_var = tk.StringVar(value="mode1")
        
        self.radio1 = tk.Radiobutton(self.top_frame, text="Sign → Speech", variable=self.mode_var, value="mode1",
                                     relief="flat", activebackground="lightblue", indicatoron=False, 
                                     width=20, font=("Arial", 12, "bold"), command=self.switch_mode)
        self.radio1.pack(side=tk.LEFT, padx=5)
        
        self.radio2 = tk.Radiobutton(self.top_frame, text="Speech → Sign", variable=self.mode_var, value="mode2",
                                     relief="flat", activebackground="lightblue", indicatoron=False, 
                                     width=20, font=("Arial", 12, "bold"), command=self.switch_mode)
        self.radio2.pack(side=tk.LEFT, padx=5)
        
        # PanedWindow
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.mode1_panel = Mode1Panel(self.paned_window, self.camera, self.tts_engine)
        self.mode2_panel = Mode2Panel(self.paned_window)
        
        self.paned_window.add(self.mode1_panel.frame, weight=1)
        self.paned_window.add(self.mode2_panel.frame, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Mode: Sign → Speech | FPS: 0 | Mic: Idle")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.switch_mode()
        
    def switch_mode(self):
        mode = self.mode_var.get()
        if mode == "mode1":
            self.mode1_panel.on_show()
            self.mode2_panel.on_hide()
        else:
            self.mode1_panel.on_hide()
            self.mode2_panel.on_show()
            
    def update_status(self, text):
        self.status_var.set(text)
        
    def on_close(self):
        self.camera.release()
        self.tts_engine.stop()
        self.mode2_panel.stop_all() 
        self.root.destroy()
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SilentBridgeApp()
    app.run()
