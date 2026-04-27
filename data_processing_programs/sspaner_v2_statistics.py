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
    df[df["CT#"] == 0][["pt_id", "Organ_Clean", "V2.0 dosevol"]]
    .drop_duplicates(subset=["pt_id","Organ_Clean"])
    .rename(columns={f"V2.0 dosevol": f"v2_base"})
)

df = df.merge(baseline, on=["pt_id", "Organ_Clean"], how="left")


df["total_v2_pct_diff"] = np.where(df["v2_base"]!=0,((df["v2_base"] - df["V2.0 dosevol"])/df["v2_base"])*100,np.nan)
df["total_v2_abs_diff"] = (df["v2_base"] - df["V2.0 dosevol"])

df_cbct = df[df["CT#"] != 0].copy()

def get_statistics(dataframe):
    array = dataframe.to_numpy()

    mean = np.nanmean(array)
    Min = np.nanmin(array)
    Max = np.nanmax(array)
    Range = Max - Min
    std = np.nanstd(array)

    return (mean, Min, Max, Range, std)


with open("v2_stats_all.txt", "a") as f:

    print("Organ Patient PID Planning_v2 Delivered_v2 Percent_difference Abs_difference", file=f)
    for _, row in df_cbct.iterrows():
        print(row["Organ_Clean"], row["Patient"], row["pt_id"], row["v2_base"], row["V2.0 dosevol"], row["total_v2_pct_diff"], row["total_v2_abs_diff"],file=f)

#print("organ column mean min max range std")

#for organ, df_organ in df_cbct.groupby(["Organ_Clean"]):
#    mean, Min, Max, Range, std = get_statistics(df_organ["total_v2_pct_diff"])
#    print(organ[0], "Percent_Difference", mean, Min, Max, Range, std)
#
#for organ, df_organ in df_cbct.groupby(["Organ_Clean"]):
#    mean, Min, Max, Range, std = get_statistics(df_organ["total_v2_abs_diff"])
#    print(organ[0], "Absolute_Difference", mean, Min, Max, Range, std)


