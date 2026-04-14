import mediapipe as mp
import cv2

class HandDetector:
    def __init__(self, static_mode=False, max_hands=2, min_det_conf=0.4, min_track_conf=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_mode,
            max_num_hands=max_hands,
            min_detection_confidence=min_det_conf,
            min_tracking_confidence=min_track_conf
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def process(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        try:
            results = self.hands.process(rgb_frame)
            return results
        except Exception as e:
            print(f"MediaPipe error: {e}")
            return None
            
    def draw_landmarks(self, frame, results):
        if results and results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
