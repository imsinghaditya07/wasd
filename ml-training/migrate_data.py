"""
Migrate gesture_data.csv from 63 features (1 hand) to 126 features (2 hands).
Pads existing single-hand data with 63 zeros for the missing second hand.
"""
import csv
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV = os.path.join(SCRIPT_DIR, 'gesture_data.csv')
BACKUP_CSV = os.path.join(SCRIPT_DIR, 'gesture_data_1hand_backup.csv')
OUTPUT_CSV = INPUT_CSV  # Overwrite in-place after backup

OLD_FEATURES = 63   # 1 hand × 21 landmarks × 3 coords
NEW_FEATURES = 126  # 2 hands × 21 landmarks × 3 coords

print("=" * 50)
print("  MIGRATING DATA: 63 features -> 126 features")
print("=" * 50)

# Read all existing data
rows = []
with open(INPUT_CSV, 'r', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if row:
            rows.append(row)

print(f"Read {len(rows)} samples from {INPUT_CSV}")

# Check if already migrated
if len(header) - 1 >= NEW_FEATURES:
    print(f"Data already has {len(header)-1} features (>= {NEW_FEATURES}). No migration needed.")
    exit()

# Backup original
import shutil
shutil.copy(INPUT_CSV, BACKUP_CSV)
print(f"Backup saved to: {BACKUP_CSV}")

# Create new header with 126 feature columns
new_header = ['label'] + [f'f{i}' for i in range(NEW_FEATURES)]

# Migrate rows: pad each 63-feature row with 63 zeros for the second hand
migrated_rows = []
for row in rows:
    label = row[0]
    features = row[1:]
    
    # Pad with zeros if needed
    if len(features) < NEW_FEATURES:
        features.extend(['0.0'] * (NEW_FEATURES - len(features)))
    
    migrated_rows.append([label] + features[:NEW_FEATURES])

# Write migrated data
with open(OUTPUT_CSV, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(new_header)
    writer.writerows(migrated_rows)

print(f"\nMigrated {len(migrated_rows)} samples to {NEW_FEATURES} features.")
print(f"Saved to: {OUTPUT_CSV}")
print("Done!")
