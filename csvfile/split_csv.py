import pandas as pd
import os

input_file = "Reviews.csv"
output_dir = "split_files"
os.makedirs(output_dir, exist_ok=True)

chunk_size = 1000

for idx, chunk in enumerate(pd.read_csv(input_file, chunksize=chunk_size), start=1):
    output_path = os.path.join(output_dir, f"reviews_part_{idx}.csv")
    chunk.to_csv(output_path, index=False, header=True)
print(f"Split csvs saved")