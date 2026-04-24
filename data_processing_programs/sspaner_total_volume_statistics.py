import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pd3_template import all_data_df

cols = [
    "Organ_Clean",
    "Patient",
    "CT#",
    "TotalVolume (cm^3)"
]

df = all_data_df[cols].copy()
df["pt_id"] = df["Patient"].str[:-1]

os.makedirs("organ_study", exist_ok=True)


baseline = (
    df[df["CT#"] == 0][["pt_id", "Organ_Clean", "TotalVolume (cm^3)"]]
    .drop_duplicates(subset=["pt_id","Organ_Clean"])
    .rename(columns={f"TotalVolume (cm^3)": f"tv_base"})
)

df = df.merge(baseline, on=["pt_id", "Organ_Clean"], how="left")


df["total_volume_pct_diff"] = ((df["tv_base"] - df["TotalVolume (cm^3)"])/df["tv_base"])*100
df["total_volume_abs_diff"] = (df["tv_base"] - df["TotalVolume (cm^3)"])

df_cbct = df[df["CT#"] != 0].copy()

df_cbct.to_csv("persisted_data/total_volume_study.csv")
