import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

labels = ["hello", "thank you", "please", "yes", "no"]
data = []
for label in labels:
    # 100 samples per label
    for _ in range(100):
        # 63 features (21 landmarks * 3 coords)
        features = np.random.normal(0, 0.1, 63).tolist()
        data.append([label] + features)

columns = ["label"] + [f"f{i}" for i in range(63)]
df = pd.DataFrame(data, columns=columns)
os.makedirs(os.path.dirname(config.TRAINING_DATA_PATH), exist_ok=True)
df.to_csv(config.TRAINING_DATA_PATH, index=False)
print(f"Generated {len(data)} dummy samples.")
