import pandas as pd
import sys
import os

if len(sys.argv) != 2:
    sys.exit(1)

file_name = sys.argv[1]
file_path = os.path.join('./output/product_reviews', file_name)

if not os.path.exists(file_path):
    print(f" File not found: {file_path}")
    sys.exit(1)

df = pd.read_parquet(file_path, engine='fastparquet')
print(f"\n Columns in {file_name}:")
print(', '.join(df.columns))
