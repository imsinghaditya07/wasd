"""
Convert Keras .h5 model to TensorFlow.js format manually.
Uses tf_keras to extract weights and topology.
Produces a clean model.json compatible with TFJS loadLayersModel.
"""

import os
import json
import numpy as np
import tf_keras as keras

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(SCRIPT_DIR, 'sign_language_model.h5')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'tfjs_model')

print(f"Loading model from {MODEL_PATH}...")
model = keras.models.load_model(MODEL_PATH)
model.summary()

os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Extract weights
weights_data = []
weight_specs = []

for layer in model.layers:
    if not layer.weights:
        continue
    for weight in layer.weights:
        w_np = weight.numpy()
        w_flat = w_np.flatten().astype(np.float32)
        
        # Clean name: remove ':0'
        name = weight.name
        if name.endswith(':0'):
            name = name[:-2]
            
        weight_specs.append({
            "name": name,
            "shape": list(w_np.shape),
            "dtype": "float32"
        })
        weights_data.append(w_flat)

# 2. Extract topology
layer_configs = []
for i, layer in enumerate(model.layers):
    config = layer.get_config()
    class_name = layer.__class__.__name__
    
    # Force batch_input_shape on the first layer
    if i == 0:
        config['batch_input_shape'] = [None, 126]
        
    layer_configs.append({
        "class_name": class_name,
        "config": config
    })

model_json = {
    "format": "layers-model",
    "generatedBy": f"keras v{keras.__version__}",
    "convertedBy": "custom_converter_v3",
    "modelTopology": {
        "keras_version": keras.__version__,
        "backend": "tensorflow",
        "model_config": {
            "class_name": "Sequential",
            "config": {
                "name": "sequential",
                "layers": layer_configs
            }
        }
    },
    "weightsManifest": [
        {
            "paths": ["group1-shard1of1.bin"],
            "weights": weight_specs
        }
    ]
}

# 3. Save files
weights_path = os.path.join(OUTPUT_DIR, "group1-shard1of1.bin")
np.concatenate(weights_data).tofile(weights_path)
print(f"Saved weights: {weights_path}")

json_path = os.path.join(OUTPUT_DIR, "model.json")
with open(json_path, 'w') as f:
    json.dump(model_json, f, indent=2)
print(f"Saved topology: {json_path}")

# Copy auxiliary files
import shutil
for f in ["label_map.json", "norm_params.json"]:
    src = os.path.join(SCRIPT_DIR, f)
    dst = os.path.join(OUTPUT_DIR, f)
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"Copied {f}")

print("\nSuccess! TFJS model is ready.")
