import cv2
import mediapipe as mp
import numpy as np
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from mode1.hand_detector import HandDetector
from mode1.feature_extractor import FeatureExtractor

def collect_data():
    os.makedirs(config.SEQUENCES_DIR, exist_ok=True)
    
    detector = HandDetector()
    extractor = FeatureExtractor()
    cap = cv2.VideoCapture(config.CAMERA_INDEX, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print("Camera not accessible.")
        return
        
    print("=== Dynamic Sign Language Collector ===")
    
    while True:
        label = input("Enter gesture label (or 'q' to quit): ").strip()
        if label.lower() == 'q':
            break
            
        # Ensure label directory exists
        path = os.path.join(config.SEQUENCES_DIR, label)
        os.makedirs(path, exist_ok=True)
        
        # Calculate how many sequences already exist to avoid overwriting
        existing_seqs = len(os.listdir(path))
        print(f"Directory ready: {path} (Already have {existing_seqs} sequences).")
        
        try:
            num_seqs = int(input("How many video sequences do you want to collect? (e.g., 30): "))
        except ValueError:
            print("Invalid number. Cancelling for this word.")
            continue
            
        print(f"\\nPress 'c' when you are ready to start recording sequences for '{label}'.")
        print("For each sequence, perform the gesture. You have a 1-second countdown between each.")
        
        waiting = True
        while waiting:
            ret, frame = cap.read()
            if not ret: break
            cv2.putText(frame, f"Press 'c' to start recording '{label}'", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow("Data Collection", frame)
            if cv2.waitKey(1) & 0xFF == ord('c'):
                waiting = False
        
        for sequence in range(existing_seqs, existing_seqs + num_seqs):
            # Countdown
            print(f"\\nGet ready for sequence {sequence+1}/{existing_seqs + num_seqs}...")
            start_time = time.time()
            while time.time() - start_time < 1.0: # 1 second pause between recordings
                ret, frame = cap.read()
                cv2.putText(frame, f"Wait...", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 3)
                cv2.imshow("Data Collection", frame)
                cv2.waitKey(1)
                
            print("RECORDING!")
            sequence_data = []
            
            # Record EXACTLY `config.SEQUENCE_LENGTH` frames
            for frame_num in range(config.SEQUENCE_LENGTH):
                ret, frame = cap.read()
                if not ret: break
                
                results = detector.process(frame)
                
                if results and results.multi_hand_landmarks:
                    detector.draw_landmarks(frame, results)
                    features = extractor.extract(results)
                    sequence_data.append(features)
                else:
                    # If hand is lost mid-recording, append zeros to keep dimension matching
                    sequence_data.append(np.zeros(63))
                    
                cv2.putText(frame, f"Recording: {frame_num+1}/{config.SEQUENCE_LENGTH}", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                cv2.imshow("Data Collection", frame)
                cv2.waitKey(1)
                
            npy_path = os.path.join(path, f"{sequence}.npy")
            np.save(npy_path, np.array(sequence_data))
            
    cap.release()
    cv2.destroyAllWindows()
    print("Collection stopped.")

if __name__ == "__main__":
    collect_data()
