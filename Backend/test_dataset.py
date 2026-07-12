import os

dataset_path = "ai_model/dataset/r4.2-1"

files = os.listdir(dataset_path)

print(f"Total files: {len(files)}")

print("\nFirst 10 files:")

for file in files[:10]:
    print(file)