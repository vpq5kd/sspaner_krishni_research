import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pd3_template import all_data_df

cols = [
    "Organ_Clean",
    "V2.0 dosevol",
    "V5.0 dosevol",
    "V10.0 dosevol",
    "Patient",
    "CT#",
    "TotalVolume (cm^3)",
    "RTOG",
    "Max_sqrt(grad(Dose)*Dose)_1",
    "Max1_Dose",
    "arm"
]

df = all_data_df[cols].copy()
df["pt_id"] = df["Patient"].str[:-1]

os.makedirs("organ_study", exist_ok=True)

organs = sorted(df["Organ_Clean"].dropna().unique())

index = 0
for organ in organs:
    for arm in [1,2]:
        organ_df = df[(df["Organ_Clean"] == organ) & (df["arm"] == arm)].copy()

        for i in [2, 5, 10]:
            baseline = (
                organ_df[organ_df["CT#"] == 0][["pt_id", f"V{i}.0 dosevol"]]
                .drop_duplicates(subset=["pt_id"])
                .rename(columns={f"V{i}.0 dosevol": f"V{i}_base"})
            )

            organ_df = organ_df.merge(baseline, on="pt_id", how="left")

            organ_df[f"V{i}_delta"] = (
                organ_df[f"V{i}.0 dosevol"] - organ_df[f"V{i}_base"]
            )

        for i in [2, 5, 10]:
            valid_pts = organ_df.groupby("pt_id")[f"V{i}.0 dosevol"].max() > 0
            valid_pts = valid_pts[valid_pts].index
            plot_df = organ_df[organ_df["pt_id"].isin(valid_pts)].copy()
            delta_array = plot_df[f"V{i}_delta"].to_numpy()
            Min = np.nanmin(delta_array)
            Max = np.nanmax(delta_array)
            Range = Max-Min
            std = np.std(delta_array)
            mean = np.mean(delta_array)
            
            if index == 0:
                print(f"organ,dose,arm,mean,std,max,min,range")
            print(f"{organ},V{i},{arm},{mean},{std},{Max},{Min},{Range}")
            
            index+=1


