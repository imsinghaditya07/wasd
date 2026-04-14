import speech_recognition as sr
import threading

class MicListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.callback = None
        
        try:
            with sr.Microphone() as source:
                pass
            self.mic_available = True
        except Exception:
            self.mic_available = False
            
    def set_on_result(self, callback_fn):
        self.callback = callback_fn
        
    def _listen_loop(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            while self.is_listening:
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    text = self.recognizer.recognize_google(audio)
                    if self.callback:
                        self.callback(text)
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    if self.callback:
                        self.callback("[Error] Check internet connection for STT")
                        
    def start_listening(self):
        if not self.mic_available:
            if self.callback:
                self.callback("[Error] No microphone detected.")
            return
            
        if not self.is_listening:
            self.is_listening = True
            self.thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.thread.start()
            
    def stop_listening(self):
        self.is_listening = False
