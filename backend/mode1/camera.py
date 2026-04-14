import cv2
import threading
from tkinter import messagebox
import numpy as np
import time

class Camera:
    def __init__(self, index=0):
        self.cap = None
        self.current_frame = None
        self.is_running = True
        
        # Auto-detect a working camera that actually shows light (not an empty black OBS virtual camera)
        valid_index = self._find_working_camera(index)
        if valid_index is None:
            # Fallback to whatever they set if all fail
            valid_index = index
            
        self.cap = cv2.VideoCapture(valid_index, cv2.CAP_DSHOW)
        
        # PRO FIX: Force MJPG and standard resolution to prevent driver blackout
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        if not self.cap.isOpened():
            print("Warning: Camera failed to open entirely.")
            
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()
        
    def _find_working_camera(self, preferred_index):
        # Try preferred first, then check common indices
        indices_to_check = [preferred_index, 0, 1, 2, 3, 4]
        for i in set(indices_to_check):
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if cap.isOpened():
                # Read a few frames to let it warm up
                for _ in range(10):
                    ret, frame = cap.read()
                    if ret and frame is not None:
                        # If average pixel brightness is > 1.0, it's not a dead black screen!
                        if np.mean(frame) > 1.0:
                            cap.release()
                            print(f"Auto-selected working camera at index {i}")
                            return i
                    time.sleep(0.05)
            cap.release()
        return None

    def _capture_loop(self):
        while self.is_running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame
                
    def get_frame(self):
        return self.current_frame.copy() if self.current_frame is not None else None
        
    def release(self):
        self.is_running = False
        if self.cap and self.cap.isOpened():
            self.cap.release()
