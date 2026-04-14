import pyttsx3
import threading
import config

class TTSEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', config.TTS_RATE)
        self.engine.setProperty('volume', config.TTS_VOLUME)
        self.lock = threading.Lock()
        
    def _speak_thread(self, text):
        with self.lock:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except RuntimeError as e:
                print(f"TTS Runtime error: {e}")
        
    def speak(self, text):
        t = threading.Thread(target=self._speak_thread, args=(text,), daemon=True)
        t.start()
        
    def stop(self):
        try:
            self.engine.stop()
        except:
            pass
