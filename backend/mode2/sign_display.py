from PIL import Image, ImageTk, ImageSequence
import tkinter as tk

class SignDisplay:
    def __init__(self, label, master):
        self.label = label
        self.master = master
        self.frames = []
        self.current_frame_idx = 0
        self.is_playing = False
        self.delay = 100
        self.after_id = None
        
    def play(self, gif_path):
        self.stop()
        
        try:
            img = Image.open(gif_path)
            self.frames = []
            
            for frame in ImageSequence.Iterator(img):
                frame_copy = frame.convert('RGBA')
                frame_copy = frame_copy.resize((300, 300), Image.Resampling.LANCZOS)
                self.frames.append(ImageTk.PhotoImage(frame_copy))
                
            self.delay = img.info.get('duration', 100)
            if self.delay == 0:
                self.delay = 100
                
            self.is_playing = True
            self.current_frame_idx = 0
            self.animate()
        except Exception as e:
            print(f"Error loading GIF {gif_path}: {e}")
            self.label.config(text=f"Sign not available (load error)", image='')
            
    def animate(self):
        if not self.is_playing or not self.frames:
            return
            
        frame = self.frames[self.current_frame_idx]
        self.label.config(image=frame, text='')
        
        self.current_frame_idx = (self.current_frame_idx + 1) % len(self.frames)
        self.after_id = self.master.after(self.delay, self.animate)
        
    def stop(self):
        self.is_playing = False
        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None
        self.frames = []
        self.label.config(image='')
