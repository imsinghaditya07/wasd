import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, Response, jsonify
from flask_cors import CORS
import cv2
import threading
import queue
import time
import config
from mode1.camera import Camera
from mode1.hand_detector import HandDetector
from mode1.feature_extractor import FeatureExtractor
from mode1.gesture_model import GestureModel

app = Flask(__name__)
CORS(app)

# Global State
current_word = "Waiting..."
conf_val = 0.0
camera = Camera()
hand_detector = HandDetector()
feature_extractor = FeatureExtractor()
gesture_model = GestureModel()
frame_queue = queue.Queue(maxsize=2)

def process_loop():
    global current_word, conf_val
    inference_cooldown = 0
    hand_lost_frames = 0
    MAX_HAND_LOST_GRACE = 60  # allow 60 frames (2 seconds) of flickering before reset
    MIN_REQUIRED_FRAMES = 30  # Start predicting after 1 second of hand data
    loop_count = 0
    
    while True:
        loop_count += 1
        if loop_count % 100 == 0:
            print(f"DEBUG: Heartbeat - Loop {loop_count} spin")
            
        frame = camera.get_frame()
        if frame is None:
            time.sleep(0.01)
            continue
            
        try:
            result = hand_detector.process(frame)
            hand_detected = result and result.multi_hand_landmarks
            
            if hand_detected:
                hand_lost_frames = 0
                hand_detector.draw_landmarks(frame, result)
                features = feature_extractor.extract(result)
                
                if features is not None:
                    # Update internal buffer
                    feature_extractor.buffer.append(features)
                    if len(feature_extractor.buffer) > config.SEQUENCE_LENGTH:
                        feature_extractor.buffer.pop(0)
                        
                    curr_len = len(feature_extractor.buffer)
                    if curr_len >= MIN_REQUIRED_FRAMES:
                        if inference_cooldown > 0:
                            inference_cooldown -= 1
                        else:
                            # 1. Prepare sequence
                            seq = np.array(feature_extractor.buffer)
                            
                            # 2. Pad to 80 frames if shorter (Self-Correction Padding)
                            if curr_len < config.SEQUENCE_LENGTH:
                                padding_len = config.SEQUENCE_LENGTH - curr_len
                                last_frame = seq[-1:]
                                padding = np.repeat(last_frame, padding_len, axis=0)
                                seq = np.concatenate([seq, padding], axis=0)
                            
                            # 3. Predict
                            prediction, conf = gesture_model.predict(seq)
                            conf_val = float(conf)
                            print(f"DEBUG: Inference Result = {prediction} ({conf:.2f})")
                            
                            if prediction:
                                current_word = prediction
                                inference_cooldown = 20 # Pause to let user finish
                            else:
                                current_word = "Analyzing..."
                    else:
                        current_word = f"Gathering... {curr_len}/{MIN_REQUIRED_FRAMES}"
            else:
                hand_lost_frames += 1
                if hand_lost_frames > MAX_HAND_LOST_GRACE:
                    if len(feature_extractor.buffer) > 0:
                        print("DEBUG: Hand lost, clearing buffer.")
                    feature_extractor.clear_buffer()
                    current_word = "Ready (No hand)"
                elif len(feature_extractor.buffer) > 0:
                    current_word = "Keep hand steady..."
        except Exception as e:
            print(f"Inference Error: {e}")
            current_word = "Error"
            
        # Draw elegant overlay
        status_color = (0, 255, 0) if "Recording" in current_word else (255, 255, 255)
        if current_word == "Ready (No hand)": status_color = (200, 200, 200)
        
        cv2.putText(frame, f"Status: {current_word}", (10, frame.shape[0]-40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        if conf_val > 0:
            cv2.putText(frame, f"Conf: {conf_val:.2f}", (10, frame.shape[0]-15), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        if not frame_queue.full():
            frame_queue.put(frame.copy())
            
        time.sleep(0.01)

def generate_frames():
    while True:
        try:
            frame = frame_queue.get(timeout=1.0)
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        except queue.Empty:
            pass

@app.route('/video_feed')
def video_feed():
    # MJPEG stream
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status')
def status():
    # Poll endpoint for React
    return jsonify({
        "current_word": current_word,
        "confidence": conf_val
    })

if __name__ == '__main__':
    print("Starting SilentBridge ML Backend on http://localhost:5000 ...")
    threading.Thread(target=process_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
