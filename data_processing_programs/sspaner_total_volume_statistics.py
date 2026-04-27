import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pd3_template import all_data_df

cols = [
    "Organ_Clean",
    "Patient",
    "CT#",
    "TotalVolume (cm^3)",
    "V2.0 dosevol"
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

def get_statistics(dataframe):
    array = dataframe.to_numpy()

    mean = np.mean(array)
    Min = np.nanmin(array)
    Max = np.nanmax(array)
    Range = Max - Min
    std = np.std(array)

    return (mean, Min, Max, Range, std)

print("organ column mean min max range std")

for organ, df_organ in df_cbct.groupby(["Organ_Clean"]):
    mean, Min, Max, Range, std = get_statistics(df_organ["total_volume_pct_diff"])
    print(organ[0], "Percent_Difference", mean, Min, Max, Range, std)

for organ, df_organ in df_cbct.groupby(["Organ_Clean"]):
    mean, Min, Max, Range, std = get_statistics(df_organ["total_volume_abs_diff"])
    print(organ[0], "Absolute_Difference", mean, Min, Max, Range, std)


