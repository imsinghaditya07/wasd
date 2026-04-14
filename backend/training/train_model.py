import os
import sys
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, BatchNormalization
from keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from keras.utils import to_categorical

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def train_model():
    if not os.path.exists(config.SEQUENCES_DIR):
        print("No sequences found.")
        return
        
    labels = sorted([f for f in os.listdir(config.SEQUENCES_DIR) if os.path.isdir(os.path.join(config.SEQUENCES_DIR, f))])
    if not labels: 
        print("No label directories found in sequences.")
        return
    
    label_map = {label:num for num, label in enumerate(labels)}
    print(f"Dataset classes: {labels}")
    
    sequences, mapped_labels = [], []
    for label in labels:
        path = os.path.join(config.SEQUENCES_DIR, label)
        count = 0
        for seq_file in os.listdir(path):
            if seq_file.endswith('.npy'):
                res = np.load(os.path.join(path, seq_file))
                
                # 1. HANDLE FEATURE DIMENSION (Legacy 63 -> 126)
                if res.shape[1] == 63:
                    padding = np.zeros((res.shape[0], 63))
                    res = np.concatenate([res, padding], axis=1)
                
                # 2. HANDLE TEMPORAL DIMENSION (Legacy 30 -> 80)
                # Pad by repeating the last frame to maintain the pose
                if res.shape[0] < config.SEQUENCE_LENGTH:
                    padding_len = config.SEQUENCE_LENGTH - res.shape[0]
                    last_frame = res[-1:]
                    padding = np.repeat(last_frame, padding_len, axis=0)
                    res = np.concatenate([res, padding], axis=0)
                elif res.shape[0] > config.SEQUENCE_LENGTH:
                    res = res[:config.SEQUENCE_LENGTH] # Trim if too long
                
                if res.shape == (config.SEQUENCE_LENGTH, 126):
                    sequences.append(res)
                    mapped_labels.append(label_map[label])
                    count += 1
        print(f" - Found {count} sequences for '{label}'")

    if not sequences: 
        print("No valid sequences found. Ensure data is collected first.")
        return

    X = np.array(sequences)
    y = to_categorical(mapped_labels).astype(int)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42, stratify=mapped_labels)
    
    print(f"Building LSTM Model... (Input Shape: {(config.SEQUENCE_LENGTH, 126)})")
    model = Sequential([
        LSTM(64, return_sequences=True, activation='tanh', input_shape=(config.SEQUENCE_LENGTH, 126)),
        BatchNormalization(),
        Dropout(0.2),
        LSTM(128, return_sequences=False, activation='tanh'),
        BatchNormalization(),
        Dropout(0.3),
        Dense(64, activation='relu'),
        Dense(len(labels), activation='softmax')
    ])
    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    # Callbacks for better training
    early_stop = EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=0.0001)
    checkpoint = ModelCheckpoint(config.MODEL_PATH_H5, monitor='val_accuracy', save_best_only=True)
    
    print("Training started...")
    history = model.fit(
        X_train, y_train, 
        epochs=150, 
        batch_size=32, 
        validation_data=(X_test, y_test),
        callbacks=[early_stop, reduce_lr, checkpoint]
    )
    
    # Save the classes
    np.save(config.MODEL_PATH_H5.replace('.keras', '_classes.npy'), np.array(labels))
    print(f"\\nTraining complete. Model saved to {config.MODEL_PATH_H5}")
    print(f"Final Validation Accuracy: {history.history['val_accuracy'][-1]:.4f}")

if __name__ == "__main__":
    train_model()
