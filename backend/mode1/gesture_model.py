import numpy as np
import os
import config
from keras.models import load_model

class GestureModel:
    def __init__(self, model_path=config.MODEL_PATH_H5, threshold=config.PREDICTION_CONFIDENCE_THRESHOLD):
        self.threshold = threshold
        self.model_loaded = False
        self.model = None
        self.classes = []
        
        if os.path.exists(model_path):
            try:
                self.model = load_model(model_path)
                classes_path = model_path.replace('.keras', '_classes.npy')
                if os.path.exists(classes_path):
                    self.classes = np.load(classes_path)
                    self.model_loaded = True
                else:
                    print(f"Classes file missing: {classes_path}")
            except Exception as e:
                print(f"Error loading LSTM model: {e}")
        else:
            print("Run training/train_model.py first to generate the Keras model.")
            
    def predict(self, feature_sequence):
        if not self.model_loaded:
            return None, 0.0
            
        # feature_sequence comes as (30, 63). We need (1, 30, 63)
        res = self.model.predict(np.expand_dims(feature_sequence, axis=0), verbose=0)[0]
        
        max_idx = np.argmax(res)
        max_prob = res[max_idx]
        
        if max_prob >= self.threshold:
            return self.classes[max_idx], float(max_prob)
        return None, float(max_prob)
