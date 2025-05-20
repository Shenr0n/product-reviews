import pandas as pd
import os

directory = './output/product_reviews'

# Loop through all .parquet files and print first 5 records from each
for filename in os.listdir(directory):
    if filename.endswith('.parquet'):
        file_path = os.path.join(directory, filename)
        df = pd.read_parquet(file_path, engine='fastparquet')
        print(df.head().to_string(index=False, header=False))
