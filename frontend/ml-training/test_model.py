import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

from google.protobuf.descriptor import FieldDescriptor
if not hasattr(FieldDescriptor, 'label') and hasattr(FieldDescriptor, '_label'):
    FieldDescriptor.label = property(lambda self: self._label)

import cv2
import numpy as np
import mediapipe as mp
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout

# Actions
DATA_PATH = os.path.join(os.getcwd(), 'MP_Data')
actions = np.array([name for name in os.listdir(DATA_PATH) if os.path.isdir(os.path.join(DATA_PATH, name))])
print(f"Loaded {len(actions)} actions: {actions}")

print("Loading model weights...")
model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30, 1662)))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))

model.load_weights('sign_language_model.h5')


# Mediapipe setups
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

def draw_styled_landmarks(image, results):
    # Draw face connections
    if results.face_landmarks:
        mp_drawing.draw_landmarks(image, results.face_landmarks, mp.solutions.face_mesh.FACEMESH_TESSELATION, 
                                 mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1), 
                                 mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)) 
    # Draw pose connections
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                 mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4), 
                                 mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)) 
    # Draw left hand connections
    if results.left_hand_landmarks:
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4), 
                                 mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)) 
    # Draw right hand connections  
    if results.right_hand_landmarks:
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4), 
                                 mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)) 


def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])

sequence = []
sentence = []
predictions = []
threshold = 0.8 # confidence threshold

print("\nStarting Camera...")
print("Press 'q' to stop.")

cap = cv2.VideoCapture(0)
# Set mediapipe model 
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False                  
        results = holistic.process(image)                 
        image.flags.writeable = True   
        
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        draw_styled_landmarks(image, results)
        
        keypoints = extract_keypoints(results)
        sequence.append(keypoints)
        sequence = sequence[-30:] # keep last 30 frames
        
        if len(sequence) == 30:
            # We predict without showing all logs per frame, or we can just predict silently
            res = model.predict(np.expand_dims(sequence, axis=0), verbose=0)[0]
            action = actions[np.argmax(res)]
            confidence = res[np.argmax(res)]
            predictions.append(np.argmax(res))
            
            # Logic for stable predictions (ensure last 10 frames predict the same)
            if len(predictions) > 10 and len(np.unique(predictions[-10:])) == 1 and np.unique(predictions[-10:])[0]==np.argmax(res):
                if confidence > threshold: 
                    if len(sentence) > 0: 
                        if action != sentence[-1]:
                            sentence.append(action)
                    else:
                        sentence.append(action)

            # keep sentence small to display
            if len(sentence) > 5: 
                sentence = sentence[-5:]
                
        # Draw top bar
        cv2.rectangle(image, (0,0), (640, 40), (245, 117, 16), -1)
        cv2.putText(image, ' '.join(sentence), (3,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, 'Press "Q" to quit', (400,30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
        
        cv2.imshow('SilentBridge Real-time Testing', image)

        # Break gracefully
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
