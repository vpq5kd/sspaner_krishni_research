from pathlib import Path
import pandas as pd
import numpy as np
import ROOT
import sys

import sspaner_pat_data_3_processing_template as template

all_data_df = template.all_data_df

kept_cols = ['Organ_Clean', 'arm', 'V1.0 dosevol', 'V2.0 dosevol', 'V5.0 dosevol']

analyzed_cols = ['V1.0 dosevol','V2.0 dosevol', 'V5.0 dosevol']
analyzed_data_df = all_data_df[kept_cols]

data_file_name = "v1-5_outputs/V1-5_stats.csv"
csv_header = "organ,col name,mean,min,max,std,range"
with open(data_file_name, "w") as f:
    f.write(f"{csv_header}\n")

for organ, df_organ in analyzed_data_df.groupby("Organ_Clean"):
    for col_name in analyzed_cols:
        col = df_organ[col_name]
        mean = col.mean()
        min_ = col.min()
        max_ = col.max()
        std = col.std()
        range_ = max_ - min_
        
        stats = f"{organ},{col_name},{mean},{min_},{max_},{std},{range_}"

        with open(data_file_name, "a") as f:
            f.write(f"{stats}\n")
        
        print(stats)

print(f"Data saved to {data_file_name}")
input("Please press enter to exit...")
