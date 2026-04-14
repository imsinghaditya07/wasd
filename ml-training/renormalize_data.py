"""
Normalize existing 126-feature data using the new Wrist-Relative + Scaling method.
Ensures existing 10k samples work with the improved inference engine.
"""
import csv
import os
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, 'gesture_data.csv')
BACKUP_PATH = os.path.join(SCRIPT_DIR, 'gesture_data_absolute_backup.csv')

if not os.path.exists(CSV_PATH):
    print("No data to re-normalize.")
    exit()

print("Backing up original data...")
import shutil
shutil.copy(CSV_PATH, BACKUP_PATH)

def process_hand(features):
    # Convert list to 21x3 array
    coords = np.array(features).reshape(21, 3)
    
    # Check if this hand is active (not all zeros)
    if np.all(coords == 0):
        return features

    # 1. Wrist relative (Wrist is landmark 0)
    wrist = coords[0]
    relative = coords - wrist
    
    # 2. Scale by max distance
    dists = np.linalg.norm(relative, axis=1)
    max_d = np.max(dists)
    
    if max_d > 0:
        scaled = relative / max_d
    else:
        scaled = relative
        
    return scaled.flatten().tolist()

print("Re-normalizing data...")
updated_rows = []
with open(CSV_PATH, 'r', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    updated_rows.append(header)
    
    count = 0
    for row in reader:
        if not row: continue
        label = row[0]
        f_all = [float(x) for x in row[1:]]
        
        # Split 126 into 63 + 63
        left = f_all[:63]
        right = f_all[63:]
        
        # Process each hand
        new_left = process_hand(left)
        new_right = process_hand(right)
        
        updated_rows.append([label] + new_left + new_right)
        count += 1
        if count % 1000 == 0: print(f"  Processed {count} rows...")

with open(CSV_PATH, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(updated_rows)

print(f"\nSuccessfully re-normalized {len(updated_rows)-1} samples!")
print("New format: Wrist-Relative + Scaled coordinates (126 features)")
