import json

path = '../public/models/sign_language_model/model.json'
with open(path, 'r', encoding='utf-8') as f:
    data = f.read()

# Fix batch shape bug
data = data.replace('"batch_shape":', '"batchInputShape":')
# Fix sequential prefix bug natively injected by tfjs converter
data = data.replace('"sequential/', '"')

with open(path, 'w', encoding='utf-8') as f:
    f.write(data)

print("Patched model.json successfully!")
