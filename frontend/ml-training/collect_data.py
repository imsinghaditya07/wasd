"""
Sign Language Data Collection Script
Uses MediaPipe Tasks API (v0.10.33+) HandLandmarker
Collects hand landmark data for A-Z, 0-9, and greeting phrases.

Each sample = 63 features (21 hand landmarks × 3 coords: x, y, z)
Data is saved to gesture_data.csv
"""

import cv2
import numpy as np
import csv
import os
import time
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions, vision
from mediapipe.tasks.python.vision import HandLandmarkerOptions, RunningMode

# ===== CONFIGURATION =====
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hand_landmarker.task')
OUTPUT_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gesture_data.csv')
SAMPLES_PER_SIGN = 100          # Number of samples to collect per sign
NUM_FEATURES = 126              # 2 hands × 21 landmarks × 3 coords (x, y, z)
COLLECTION_DELAY_SEC = 3        # Countdown before recording each sign
FRAME_INTERVAL_MS = 100         # Minimum ms between captured samples

# Signs to collect (Expanded to 150 for common daily use)
import string
SIGNS = sorted(list(set(
    list(string.ascii_uppercase) +          # A-Z (26)
    [str(i) for i in range(10)] +           # 0-9 (10)
    ['HELLO', 'THANK YOU', 'HOW ARE YOU', 'GOOD AFTERNOON', 'GOOD MORNING', 'GOOD EVENING', 'GOOD NIGHT', 'WELCOME'] +
    ['YES', 'NO', 'PLEASE', 'SORRY', 'HELP', 'STOP', 'I LOVE YOU', 'GOODBYE', 'OK', 'WATER', 'FOOD', 'BATHROOM'] +
    ['I AM FINE', 'MY NAME IS', 'HAPPY', 'SAD', 'EMERGENCY', 'DOCTOR', 'FAMILY'] +
    ['I UNDERSTAND', 'I DON\'T KNOW', 'WAIT', 'AGAIN', 'MORE', 'FINISHED', 'COME', 'GO', 'SIT', 'STAND', 'EXCITED', 'CONFUSED', 'ANGRY'] +
    ['HOME', 'SCHOOL', 'WORK', 'EAT', 'DRINK', 'SLEEP', 'MOTHER', 'FATHER', 'BROTHER', 'SISTER', 'BABY', 'FRIEND', 'TEACHER', 'STUDENT', 'HUNGRY', 'TIRED', 'SCARED', 'SURPRISED', 'SICK', 'PAIN'] +
    # --- NEW SIGNS (Common Daily Life) ---
    ['WHO', 'WHAT', 'WHERE', 'WHEN', 'WHY', 'HOW', 'TODAY', 'TOMORROW', 'YESTERDAY', 'NOW', 'FUTURE', 'PAST', 'DAY', 'NIGHT', 'WEEK', 'MONTH'] +
    ['GRANDMA', 'GRANDPA', 'HUSBAND', 'WIFE', 'COUSIN', 'CAR', 'DRIVE', 'BUS', 'TRAIN', 'BICYCLE'] +
    ['RED', 'BLUE', 'GREEN', 'YELLOW', 'BLACK', 'WHITE', 'PINK', 'PURPLE', 'ORANGE'] +
    ['WANT', 'NEED', 'LIKE', 'LEARN', 'KNOW', 'FORGET', 'REMEMBER', 'BUSY', 'GOOD', 'BAD', 'HOT', 'COLD', 'SAME', 'DIFFERENT', 'BIG', 'SMALL']
)))

def extract_hand_features(detection_result):
    """Extract 126 features from both hands (left 63 + right 63).
    Implements Relative Normalization:
    1. Wrist is moved to (0,0,0)
    2. All landmarks scaled relative to max distance from wrist
    """
    if not detection_result.hand_landmarks:
        return None

    left_features = [0.0] * 63
    right_features = [0.0] * 63

    for i, hand_landmarks in enumerate(detection_result.hand_landmarks):
        # 1. Wrist-Relative Normalization
        wrist = hand_landmarks[0]
        temp_coords = []
        for lm in hand_landmarks:
            temp_coords.append([lm.x - wrist.x, lm.y - wrist.y, lm.z - wrist.z])
        
        # 2. Scaling Normalization (Make scale independent)
        # Find max distance from wrist to any landmark
        max_dist = 0
        for coord in temp_coords:
            dist = (coord[0]**2 + coord[1]**2 + coord[2]**2)**0.5
            if dist > max_dist: max_dist = dist
        
        # Scale all coordinates
        final_coords = []
        if max_dist > 0:
            for coord in temp_coords:
                final_coords.extend([coord[0]/max_dist, coord[1]/max_dist, coord[2]/max_dist])
        else:
            for coord in temp_coords:
                final_coords.extend([0.0, 0.0, 0.0])

        # Determine handedness
        if detection_result.handedness and i < len(detection_result.handedness):
            hand_label = detection_result.handedness[i][0].category_name
        else:
            hand_label = 'Right' if i == 0 else 'Left'

        if hand_label == 'Left':
            left_features = final_coords
        else:
            right_features = final_coords

    return left_features + right_features

def main():
    # ... rest of main ...

def main():
    print("=" * 60)
    print("   SIGN LANGUAGE DATA COLLECTION (MediaPipe Tasks API)")
    print("=" * 60)
    print(f"\nSigns to collect: {len(SIGNS)} total")
    print(f"Samples per sign: {SAMPLES_PER_SIGN}")
    print(f"Output file: {OUTPUT_CSV}\n")

    # Check if model file exists
    if not os.path.exists(MODEL_PATH):
        print(f"ERROR: Model file not found at {MODEL_PATH}")
        print("Download it: https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task")
        return

    # Setup HandLandmarker (2 hands for two-hand signs)
    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        num_hands=2,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    detector = vision.HandLandmarker.create_from_options(options)

    # Check for existing data to enable resume
    existing_data = {}
    header = ['label'] + [f'f{i}' for i in range(NUM_FEATURES)]

    if os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                if row:
                    label = row[0]
                    existing_data[label] = existing_data.get(label, 0) + 1
        print("Found existing data:")
        for label, count in existing_data.items():
            print(f"  {label}: {count} samples")
        print()

    # Open CSV in append mode
    file_exists = os.path.exists(OUTPUT_CSV) and os.path.getsize(OUTPUT_CSV) > 0
    csvfile = open(OUTPUT_CSV, 'a', newline='')
    writer = csv.writer(csvfile)
    if not file_exists:
        writer.writerow(header)

    # Open camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Camera not accessible!")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("Camera opened. Press 'q' at any time to quit and save progress.\n")

    try:
        for sign_idx, sign in enumerate(SIGNS):
            # Check how many samples we already have
            already_collected = existing_data.get(sign, 0)
            remaining = SAMPLES_PER_SIGN - already_collected

            if remaining <= 0:
                print(f"[{sign_idx+1}/{len(SIGNS)}] '{sign}' already has {already_collected} samples. SKIPPING.")
                continue

            print(f"\n{'='*50}")
            print(f"[{sign_idx+1}/{len(SIGNS)}] NEXT SIGN: '{sign}'")
            print(f"Need {remaining} more samples (have {already_collected}/{SAMPLES_PER_SIGN})")
            print(f"{'='*50}")

            # Countdown
            quit_flag = False
            for countdown in range(COLLECTION_DELAY_SEC, 0, -1):
                start = time.time()
                while time.time() - start < 1.0:
                    ret, frame = cap.read()
                    if not ret:
                        continue
                    frame = cv2.flip(frame, 1)  # Mirror for natural feel

                    # Display countdown
                    cv2.rectangle(frame, (0, 0), (640, 80), (0, 0, 0), -1)
                    cv2.putText(frame, f"Get ready for: '{sign}'", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                    cv2.putText(frame, f"Starting in {countdown}...", (10, 65),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
                    cv2.imshow('Sign Language Data Collection', frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        quit_flag = True
                        break
                if quit_flag:
                    break

            if quit_flag:
                print("\nUser pressed 'q' - saving progress and exiting...")
                break

            # COLLECT SAMPLES
            collected = 0
            last_capture_time = 0

            while collected < remaining:
                ret, frame = cap.read()
                if not ret:
                    continue
                frame = cv2.flip(frame, 1)

                # Convert to MediaPipe Image
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

                # Detect hand
                result = detector.detect(mp_image)
                features = extract_hand_features(result)

                # Draw hand landmarks on frame (green=left, blue=right)
                if result.hand_landmarks:
                    colors = [(0, 255, 0), (255, 100, 0)]  # Green for left, Blue for right
                    for hand_idx, hand_lms in enumerate(result.hand_landmarks):
                        color = colors[hand_idx % 2]
                        for lm in hand_lms:
                            x_px = int(lm.x * frame.shape[1])
                            y_px = int(lm.y * frame.shape[0])
                            cv2.circle(frame, (x_px, y_px), 4, color, -1)
                    hands_detected = len(result.hand_landmarks)
                    cv2.putText(frame, f"Hands: {hands_detected}/2", (480, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

                current_time = time.time() * 1000
                if features and (current_time - last_capture_time) >= FRAME_INTERVAL_MS:
                    writer.writerow([sign] + features)
                    csvfile.flush()
                    collected += 1
                    last_capture_time = current_time

                # Display info
                total_done = already_collected + collected
                cv2.rectangle(frame, (0, 0), (640, 80), (0, 0, 0), -1)
                cv2.putText(frame, f"Recording: '{sign}'", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                cv2.putText(frame, f"Sample {total_done}/{SAMPLES_PER_SIGN}", (10, 65),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

                # Progress bar
                progress = total_done / SAMPLES_PER_SIGN
                bar_width = 300
                cv2.rectangle(frame, (10, 440), (10 + bar_width, 460), (50, 50, 50), -1)
                cv2.rectangle(frame, (10, 440), (10 + int(bar_width * progress), 460), (0, 255, 0), -1)

                if not features:
                    cv2.putText(frame, "NO HAND DETECTED - Show your hand!", (10, 420),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                cv2.imshow('Sign Language Data Collection', frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    quit_flag = True
                    break

            if quit_flag:
                print(f"\nPaused during '{sign}'. Collected {collected} new samples.")
                print("Run this script again to resume from where you stopped!")
                break

            # Update existing_data for skip logic
            existing_data[sign] = already_collected + collected
            print(f"  Done collecting '{sign}': {collected} new samples ({existing_data[sign]} total)")

    finally:
        csvfile.close()
        cap.release()
        cv2.destroyAllWindows()
        detector.close()

    print("\n" + "=" * 60)
    print("DATA COLLECTION COMPLETE!")
    print(f"Data saved to: {OUTPUT_CSV}")
    print("=" * 60)

if __name__ == '__main__':
    main()
