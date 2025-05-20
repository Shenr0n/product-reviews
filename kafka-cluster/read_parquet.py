import pandas as pd
import os

dir_path = './output/product_reviews'

for filename in os.listdir(dir_path):
    if filename.endswith('.parquet'):
        file_path = os.path.join(dir_path, filename)
        df = pd.read_parquet(file_path, engine='fastparquet')
        print(df.head().to_string(index=False, header=False))
