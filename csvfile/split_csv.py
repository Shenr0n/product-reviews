import pandas as pd
import os

input_file = "Reviews.csv"
output_dir = "split_files"

#create directory if not exists
os.makedirs(output_dir, exist_ok=True)

#chunk of 1000 records which will be used to create new files for each chunk
chunk_size = 1000

# iterate over the Reviews csv file and split it
for idx, chunk in enumerate(pd.read_csv(input_file, chunksize=chunk_size), start=1):
    output_path = os.path.join(output_dir, f"reviews_part_{idx}.csv")
    chunk.to_csv(output_path, index=False, header=True)
print(f"Split csvs saved")