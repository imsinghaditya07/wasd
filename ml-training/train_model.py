"""
Sign Language Model Training Script
Trains a neural network on gesture_data.csv (63 features per sample).
Uses a Dense (MLP) architecture for static hand sign classification.
Exports to TensorFlow.js format for web integration.

Signs: A-Z, 0-9, HELLO, THANK YOU, HOW ARE YOU, GOOD AFTERNOON
"""

import numpy as np
import csv
import os
import json
from sklearn.model_selection import train_test_split
from tf_keras.models import Sequential
from tf_keras.layers import Dense, Dropout, BatchNormalization, Input
from tf_keras.utils import to_categorical
from tf_keras.callbacks import EarlyStopping, ReduceLROnPlateau

# ===== CONFIGURATION =====
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, 'gesture_data.csv')
MODEL_SAVE_PATH = os.path.join(SCRIPT_DIR, 'sign_language_model.h5')
TFJS_OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'tfjs_model')
LABEL_MAP_PATH = os.path.join(SCRIPT_DIR, 'label_map.json')
NUM_FEATURES = 126
EPOCHS = 150
BATCH_SIZE = 32
TEST_SPLIT = 0.15
VALIDATION_SPLIT = 0.15

def load_data(csv_path):
    """Load gesture data from CSV file."""
    features = []
    labels = []
    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader)  # skip header
        for row in reader:
            if not row or len(row) < NUM_FEATURES + 1:
                continue
            labels.append(row[0])
            features.append([float(x) for x in row[1:NUM_FEATURES+1]])
    return np.array(features), labels

def main():
    print("=" * 60)
    print("   SIGN LANGUAGE MODEL TRAINING")
    print("=" * 60)

    # 1. LOAD DATA
    if not os.path.exists(DATA_PATH):
        print(f"\nERROR: No data file found at {DATA_PATH}")
        print("Run collect_data.py first to collect training data!")
        return

    print(f"\nLoading data from: {DATA_PATH}")
    X, raw_labels = load_data(DATA_PATH)
    print(f"Total samples: {X.shape[0]}")
    print(f"Features per sample: {X.shape[1]}")

    # 2. ENCODE LABELS
    unique_labels = sorted(set(raw_labels))
    label_to_idx = {label: idx for idx, label in enumerate(unique_labels)}
    idx_to_label = {idx: label for label, idx in label_to_idx.items()}
    num_classes = len(unique_labels)

    print(f"\nDetected {num_classes} sign classes:")
    label_counts = {}
    for l in raw_labels:
        label_counts[l] = label_counts.get(l, 0) + 1
    for label in unique_labels:
        print(f"  {label}: {label_counts[label]} samples")

    y_numeric = np.array([label_to_idx[l] for l in raw_labels])
    y = to_categorical(y_numeric, num_classes=num_classes)

    # Save label map for inference
    with open(LABEL_MAP_PATH, 'w') as f:
        json.dump(idx_to_label, f, indent=2)
    print(f"\nLabel map saved to: {LABEL_MAP_PATH}")

    # 3. NORMALIZE FEATURES
    X_mean = X.mean(axis=0)
    X_std = X.std(axis=0) + 1e-8  # Avoid division by zero
    X_normalized = (X - X_mean) / X_std

    # Save normalization params for inference
    norm_params_path = os.path.join(SCRIPT_DIR, 'norm_params.json')
    with open(norm_params_path, 'w') as f:
        json.dump({'mean': X_mean.tolist(), 'std': X_std.tolist()}, f)
    print(f"Normalization params saved to: {norm_params_path}")

    # 4. SPLIT DATA
    X_train, X_test, y_train, y_test = train_test_split(
        X_normalized, y, test_size=TEST_SPLIT, random_state=42, stratify=y_numeric
    )
    print(f"\nTraining samples: {X_train.shape[0]}")
    print(f"Testing samples: {X_test.shape[0]}")

    # 5. BUILD MODEL (Advanced architecture for 150+ classes)
    print("\n--- Model Architecture ---")
    from tf_keras.layers import GaussianNoise
    from tf_keras.regularizers import l1_l2
    
    model = Sequential([
        Input(shape=(NUM_FEATURES,)),
        GaussianNoise(0.01), # Simulates camera jitter for better robustness
        Dense(512, activation='relu', kernel_regularizer=l1_l2(l1=1e-5, l2=1e-4)),
        BatchNormalization(),
        Dropout(0.4),
        Dense(256, activation='relu', kernel_regularizer=l1_l2(l1=1e-5, l2=1e-4)),
        BatchNormalization(),
        Dropout(0.4),
        Dense(128, activation='relu'),
        BatchNormalization(),
        Dropout(0.3),
        Dense(64, activation='relu'),
        BatchNormalization(),
        Dense(num_classes, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    model.summary()

    # 5b. DATA AUGMENTATION - Add noise copies to training data
    print("\nAugmenting training data with noise injection...")
    noise_copies = 3
    X_aug = [X_train]
    y_aug = [y_train]
    for _ in range(noise_copies):
        noise = np.random.normal(0, 0.02, X_train.shape)
        X_aug.append(X_train + noise)
        y_aug.append(y_train)
    X_train = np.vstack(X_aug)
    y_train = np.vstack(y_aug)
    print(f"Augmented training samples: {X_train.shape[0]}")

    # 6. TRAIN MODEL
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=30, restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10, min_lr=1e-6, verbose=1),
    ]

    EPOCHS = 300
    history = model.fit(
        X_train, y_train,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_split=VALIDATION_SPLIT,
        callbacks=callbacks,
        verbose=1
    )

    # 7. EVALUATE
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"\n{'='*40}")
    print(f"Test Loss: {loss:.4f}")
    print(f"Test Accuracy: {accuracy*100:.2f}%")
    print(f"{'='*40}")

    # 8. SAVE KERAS MODEL
    model.save(MODEL_SAVE_PATH)
    print(f"\nKeras model saved to: {MODEL_SAVE_PATH}")

    # 9. CONVERT TO TENSORFLOW.JS
    print("\nConverting to TensorFlow.js format...")
    try:
        import tensorflowjs as tfjs
        os.makedirs(TFJS_OUTPUT_DIR, exist_ok=True)
        tfjs.converters.save_keras_model(model, TFJS_OUTPUT_DIR)
        print(f"TFJS model saved to: {TFJS_OUTPUT_DIR}/")

        # Copy label_map and norm_params to tfjs output for easy web access
        import shutil
        shutil.copy(LABEL_MAP_PATH, os.path.join(TFJS_OUTPUT_DIR, 'label_map.json'))
        shutil.copy(norm_params_path, os.path.join(TFJS_OUTPUT_DIR, 'norm_params.json'))
        print("Copied label_map.json and norm_params.json to TFJS output folder.")
    except ImportError:
        print("WARNING: tensorflowjs not installed. Skipping TFJS export.")
        print("Install with: pip install tensorflowjs")
        print("Then run: tensorflowjs_converter --input_format keras "
              f"{MODEL_SAVE_PATH} {TFJS_OUTPUT_DIR}")

    print("\n" + "=" * 60)
    print("TRAINING COMPLETE!")
    print("=" * 60)

if __name__ == '__main__':
    main()
