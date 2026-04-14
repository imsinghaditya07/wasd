import numpy as np
import config

class FeatureExtractor:
    def __init__(self, sequence_length=config.SEQUENCE_LENGTH):
        self.sequence_length = sequence_length
        self.buffer = []

    def extract(self, results):
        if not results or not results.multi_hand_landmarks:
            return None
            
        # Initialize 126 features (63 for Left, 63 for Right)
        # We use MediaPipe's classification to keep the order consistent
        full_features = {"Left": np.zeros(63), "Right": np.zeros(63)}
        
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Get label (Left or Right)
            label = results.multi_handedness[i].classification[0].label # "Left" or "Right"
            
            wrist = hand_landmarks.landmark[0]
            wx, wy, wz = wrist.x, wrist.y, wrist.z
            
            # Stability fix: Scale by the distance between wrist and index finger base (joint 5)
            index_mcp = hand_landmarks.landmark[5]
            scale = np.sqrt((index_mcp.x - wx)**2 + (index_mcp.y - wy)**2 + (index_mcp.z - wz)**2)
            if scale < 1e-6: scale = 1.0 # prevent div zero
            
            features = []
            for lm in hand_landmarks.landmark:
                rel_x = (lm.x - wx) / scale
                rel_y = (lm.y - wy) / scale
                rel_z = (lm.z - wz) / scale
                features.extend([rel_x, rel_y, rel_z])
            
            full_features[label] = np.array(features, dtype=np.float32)
            
        # PATCH: If only one hand was detected, map its features to BOTH slots
        # to ensure compatibility with mirrored cameras and different signing hands.
        if len(results.multi_hand_landmarks) == 1:
            detected_label = results.multi_handedness[0].classification[0].label
            other_label = "Right" if detected_label == "Left" else "Left"
            full_features[other_label] = full_features[detected_label]
            
        # Concatenate: Left 63 + Right 63 = 126 total
        return np.concatenate([full_features["Left"], full_features["Right"]])

    def append_and_get_sequence(self, features):
        self.buffer.append(features)
        if len(self.buffer) > self.sequence_length:
            self.buffer.pop(0)
            
        if len(self.buffer) == self.sequence_length:
            return np.array(self.buffer)
        return None
        
    def clear_buffer(self):
        self.buffer = []
