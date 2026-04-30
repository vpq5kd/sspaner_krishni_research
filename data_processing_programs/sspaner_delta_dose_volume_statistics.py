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

results = []
for (organ, arm), group in df.groupby(["Organ_Clean","arm"]):
    row = {"organ": organ, "arm": arm}
    for i in [2,5,10]:
        baseline = (
            group[group["CT#"] == 0][["pt_id", f"V{i}.0 dosevol"]]
            .rename(columns={f"V{i}.0 dosevol": f"V{i}_base"})
        )

        groupi = group.merge(baseline, on="pt_id", how="left")

        groupi[f"V{i}_delta"] = (
            groupi[f"V{i}.0 dosevol"] - groupi[f"V{i}_base"]
        )

        delivered_delta_mean = groupi[groupi["CT#"] != 0][f"V{i}_delta"].mean()
        row[f"V{i}"] = delivered_delta_mean

    results.append(row)



table_df = pd.DataFrame(results)
final_table = table_df.pivot(index="organ",columns="arm",values=[f"V{i}" for i in [2,5,10]])

final_table.columns = [
    f"A{arm}, {threshold}"
    for threshold, arm in final_table.columns
]

final_table.to_csv("persisted_data/table1.csv")


    


