import tkinter as tk
from tkinter import ttk
import config
from mode2.mic_listener import MicListener
from mode2.nlp_processor import NLPProcessor
from mode2.sign_mapper import SignMapper
from mode2.sign_display import SignDisplay

class Mode2Panel:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        
        self.mic_listener = MicListener()
        self.mic_listener.set_on_result(self.on_speech_result)
        
        self.nlp_processor = NLPProcessor()
        self.sign_mapper = SignMapper()
        
        self.is_listening = False
        self.word_queue = []
        self.is_playing = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # Top controls
        ctrl_frame = tk.Frame(self.frame)
        ctrl_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
        
        self.mic_status = tk.Canvas(ctrl_frame, width=30, height=30)
        self.mic_status.pack(side=tk.LEFT, padx=10)
        self.mic_oval = self.mic_status.create_oval(5, 5, 25, 25, fill="grey")
        
        self.listen_btn = tk.Button(ctrl_frame, text="Start Listening", command=self.toggle_listen, font=("Arial", 14))
        self.listen_btn.pack(side=tk.LEFT)
        
        # Transcript area
        self.transcript = tk.Text(self.frame, height=5, font=("Arial", 12))
        self.transcript.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        # Sign display area
        self.display_label = tk.Label(self.frame, width=60, height=20, bg="black", text="Waiting for speech...", fg="white", font=("Arial", 16))
        self.display_label.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.sign_display = SignDisplay(self.display_label, self.frame)
        
    def toggle_listen(self):
        if self.is_listening:
            self.mic_listener.stop_listening()
            self.listen_btn.config(text="Start Listening")
            self.mic_status.itemconfig(self.mic_oval, fill="grey")
            self.is_listening = False
        else:
            self.mic_listener.start_listening()
            self.listen_btn.config(text="Stop Listening")
            self.mic_status.itemconfig(self.mic_oval, fill="red")
            self.is_listening = True
            
    def on_speech_result(self, text):
        if text.startswith("[Error]") or text.startswith("[Warning]"):
            self.transcript.insert(tk.END, text + "\\n")
            self.transcript.see(tk.END)
            return
            
        self.transcript.insert(tk.END, text + "\\n")
        self.transcript.see(tk.END)
        
        words = self.nlp_processor.process(text)
        self.word_queue.extend(words)
        
        if not self.is_playing:
            self.play_next_word()
            
    def play_next_word(self):
        if not self.word_queue:
            self.is_playing = False
            self.sign_display.stop()
            self.display_label.config(text="Waiting for speech...", image='')
            return
            
        self.is_playing = True
        word = self.word_queue.pop(0)
        
        gif_path, match_type = self.sign_mapper.lookup(word)
        if gif_path:
            self.sign_display.play(gif_path)
            self.frame.after(1500, self.pause_between_signs)
        else:
            self.sign_display.stop()
            self.display_label.config(text=f"Sign not available for: [{word}]", image='')
            self.frame.after(2000, self.play_next_word)
            
    def pause_between_signs(self):
        self.sign_display.stop()
        self.display_label.config(text="", image='')
        self.frame.after(config.SIGN_DISPLAY_DELAY_MS, self.play_next_word)
        
    def on_show(self):
        pass
        
    def on_hide(self):
        pass
        
    def stop_all(self):
        if self.is_listening:
            self.toggle_listen()
        self.sign_display.stop()
