import cv2
import numpy as np
import os
import sys
import time
from pathlib import Path

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from mode1.hand_detector import HandDetector
from mode1.feature_extractor import FeatureExtractor

def bulk_collect():
    # Predefined lists
    ALPHABET = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    GREETINGS = ["Good Morning", "Good Night", "Welcome", "How are you", "I am fine", "Goodbye", "Help", "Sorry"]
    
    # Combined target list
    target_signs = ALPHABET + GREETINGS
    
    # Setup
    detector = HandDetector()
    extractor = FeatureExtractor()
    cap = cv2.VideoCapture(config.CAMERA_INDEX, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print("Error: Camera not accessible.")
        return

    print("\n" + "="*50)
    print("SILENTBRIDGE BULK SIGN COLLECTOR")
    print("="*50)
    print(f"Goal: Collect 30 sequences for {len(target_signs)} signs.")
    print("Instructions:")
    print("1. We will go through the list one by one.")
    print("2. If you already have data for a sign, we can skip it.")
    print("3. Press 'c' to record, 's' to skip, 'q' to quit.")
    print("="*50 + "\n")

    for sign in target_signs:
        path = os.path.join(config.SEQUENCES_DIR, sign)
        os.makedirs(path, exist_ok=True)
        
        existing_count = len([f for f in os.listdir(path) if f.endswith('.npy')])
        
        if existing_count >= 30:
            print(f"[SKIP] Skipping '{sign}' (Already have {existing_count} sequences)")
            continue
            
        print(f"\n[NEXT] NEXT SIGN: '{sign}'")
        print(f"Current count: {existing_count}/30")
        print(f"Options: [C] Start Recording | [S] Skip | [Q] Exit")
        
        # Idle/Wait for command
        action = None
        while True:
            ret, frame = cap.read()
            if not ret: break
            
            display = frame.copy()
            cv2.rectangle(display, (0, 0), (640, 60), (0,0,0), -1)
            cv2.putText(display, f"SIGN: {sign.upper()}", (20, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            cv2.putText(display, f"[C] Record  [S] Skip  [Q] Quit", (350, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            cv2.imshow("Bulk Collection", display)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):
                action = 'collect'
                break
            if key == ord('s'):
                action = 'skip'
                break
            if key == ord('q'):
                action = 'quit'
                break
        
        if action == 'quit': break
        if action == 'skip': continue
        
        # Recording loop for 30 sequences
        to_collect = 30 - existing_count
        for seq_idx in range(existing_count, 30):
            # 1. Countdown
            start_time = time.time()
            while time.time() - start_time < 0.8:
                ret, frame = cap.read()
                cv2.putText(frame, f"GET READY: {sign} ({seq_idx+1}/30)", (10, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 0), 3)
                cv2.imshow("Bulk Collection", frame)
                cv2.waitKey(1)

            # 2. Capture sequence
            sequence_data = []
            print(f"Recording {sign} ({seq_idx+1}/30)...", end="\r")
            
            for f_num in range(config.SEQUENCE_LENGTH):
                ret, frame = cap.read()
                if not ret: break
                
                res = detector.process(frame)
                if res and res.multi_hand_landmarks:
                    detector.draw_landmarks(frame, res)
                    feats = extractor.extract(res)
                    sequence_data.append(feats)
                else:
                    sequence_data.append(np.zeros(126))
                
                cv2.circle(frame, (30, 30), 10, (0, 0, 255), -1) # "REC" dot
                cv2.putText(frame, f"REC: {f_num+1}/{config.SEQUENCE_LENGTH}", (50, 40), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.imshow("Bulk Collection", frame)
                cv2.waitKey(1)
            
            # Save
            np.save(os.path.join(path, f"{seq_idx}.npy"), np.array(sequence_data))
            
    cap.release()
    cv2.destroyAllWindows()
    print("\n\n[DONE] Session Finished!")

if __name__ == "__main__":
    bulk_collect()
