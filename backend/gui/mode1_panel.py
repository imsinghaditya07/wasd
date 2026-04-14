import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import config
from mode1.hand_detector import HandDetector
from mode1.feature_extractor import FeatureExtractor
from mode1.gesture_model import GestureModel
from tkinter import messagebox
import time
import threading
import queue

class Mode1Panel:
    def __init__(self, parent, camera, tts_engine):
        self.frame = tk.Frame(parent)
        self.camera = camera
        self.tts_engine = tts_engine
        
        self.hand_detector = HandDetector()
        self.feature_extractor = FeatureExtractor()
        self.gesture_model = GestureModel()
        
        self.current_word = None
        self.is_active = False
        
        # Threading infrastructure to prevent GUI freezing
        self.frame_queue = queue.Queue(maxsize=2)
        self.processing_thread = None
        
        if not self.gesture_model.model_loaded:
            messagebox.showwarning("Model Missing", "Gesture model not found. Run training/train_model.py to enable Sign → Speech mode.")

        self.create_widgets()
        
    def create_widgets(self):
        # Video feed
        self.video_label = tk.Label(self.frame)
        self.video_label.pack(side=tk.TOP, pady=10)
        
        # Word display
        self.word_label = tk.Label(self.frame, text="Waiting...", font=("Arial", 32, "bold"))
        self.word_label.pack(side=tk.TOP, pady=10)
        
        # Speak button
        self.speak_btn = tk.Button(self.frame, text="Speak", font=("Arial", 16), command=self.speak_word)
        self.speak_btn.pack(side=tk.TOP, pady=10)
        
        # Confidence meter
        conf_frame = tk.Frame(self.frame)
        conf_frame.pack(side=tk.TOP, pady=10)
        tk.Label(conf_frame, text="Confidence: ").pack(side=tk.LEFT)
        self.conf_bar = ttk.Progressbar(conf_frame, orient="horizontal", length=200, mode="determinate")
        self.conf_bar.pack(side=tk.LEFT)
        
    def speak_word(self):
        if self.current_word and self.current_word not in ["No hand detected", "Waiting...", "Unknown", "Processing Error"]:
            if not self.current_word.startswith("Buffering"):
                self.tts_engine.speak(self.current_word)
            
    def on_show(self):
        if not self.is_active:
            self.is_active = True
            # Clear stale data
            with self.frame_queue.mutex:
                self.frame_queue.queue.clear()
                
            self.processing_thread = threading.Thread(target=self.process_loop, daemon=True)
            self.processing_thread.start()
            self.update_gui()
        
    def on_hide(self):
        self.is_active = False
        if self.processing_thread:
            self.processing_thread.join(timeout=1.0)
            
    def process_loop(self):
        inference_cooldown = 0
        conf_val = 0
        current_word = "Waiting..."
        
        while self.is_active:
            frame = self.camera.get_frame()
            if frame is None:
                time.sleep(0.01)
                continue
                
            try:
                result = self.hand_detector.process(frame)
                if result:
                    self.hand_detector.draw_landmarks(frame, result)
                    features = self.feature_extractor.extract(result)
                    
                    if features is not None:
                        seq = self.feature_extractor.append_and_get_sequence(features)
                        if seq is not None:
                            if inference_cooldown > 0:
                                inference_cooldown -= 1
                            else:
                                prediction, conf = self.gesture_model.predict(seq)
                                conf_val = conf
                                if prediction:
                                    current_word = prediction
                                    # Anti-spam: wait 15 frames after successful prediction before predicting again
                                    inference_cooldown = 15 
                                    self.feature_extractor.clear_buffer() # Clear to start fresh gesture
                                else:
                                    current_word = "Unknown"
                        else:
                            current_word = f"Buffering... {len(self.feature_extractor.buffer)}/30"
                            conf_val = 0
                    else:
                        self.feature_extractor.clear_buffer()
                        current_word = "No hand detected"
                        conf_val = 0
                else:
                    self.feature_extractor.clear_buffer()
                    current_word = "No hand detected"
                    conf_val = 0
            except Exception as e:
                print(f"Error in processing frame: {e}")
                current_word = "Processing Error"
            
            self.current_word = current_word
            
            # Overlay text
            word_to_show = current_word if current_word else "Waiting..."
            cv2.putText(frame, word_to_show, (10, frame.shape[0]-20), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
            
            if not self.frame_queue.full():
                self.frame_queue.put((frame.copy(), current_word, conf_val))
                
            time.sleep(0.005) # Prevent maxing out the CPU loop
            
    def update_gui(self):
        if not self.is_active:
            return
            
        try:
            # Process everything in queue to keep up with video
            while True:
                frame, current_word, conf = self.frame_queue.get_nowait()
                # Update GUI with the MOST RECENT frame pulled
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb_frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
                
                word_to_show = current_word if current_word else "Waiting..."
                self.word_label.config(text=word_to_show)
                self.conf_bar["value"] = conf * 100
        except queue.Empty:
            pass
            
        self.frame.after(config.GUI_UPDATE_INTERVAL_MS, self.update_gui)
