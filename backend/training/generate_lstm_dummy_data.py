import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def generate():
    labels = ["hello", "thank you", "please", "yes", "no"]
    samples_per_label = 30
    seq_len = config.SEQUENCE_LENGTH
    
    os.makedirs(config.SEQUENCES_DIR, exist_ok=True)
    
    for label in labels:
        path = os.path.join(config.SEQUENCES_DIR, label)
        os.makedirs(path, exist_ok=True)
        
        for i in range(samples_per_label):
            base_curve = np.linspace(0, 1, seq_len)
            noise = np.random.normal(0, 0.05, (seq_len, 63))
            
            if label == "hello":
                noise[:, 0] += base_curve
            elif label == "thank you":
                noise[:, 1] -= base_curve
            elif label == "please":
                noise[:, 2] += base_curve * 2
            elif label == "yes":
                noise[:, 3] -= base_curve * 2
                
            np.save(os.path.join(path, f"{i}.npy"), noise)
            
    print(f"Generated {samples_per_label} LSTM sequences for {len(labels)} classes.")

if __name__ == "__main__":
    generate()
