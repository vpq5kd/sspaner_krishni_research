from pathlib import Path
import pandas as pd

pat_data_3 = Path("./pat_data_3")

for folder in pat_data_3.iterdir():
    if folder.is_dir():
        for file in folder.glob("*.csv"):
            df = pd.read_csv(file)
            print(df.head())
