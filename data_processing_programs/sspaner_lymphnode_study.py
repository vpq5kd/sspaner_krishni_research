import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pd3_template import all_data_df
import sys

lymphnode_df = all_data_df[all_data_df["Organ_Clean"] == "LN"]
cols = ['V2.0 dosevol','V5.0 dosevol', 'V10.0 dosevol', 'Patient', 'CT#', 'TotalVolume (cm^3)', 'RTOG']

lymphnode_df = lymphnode_df[cols]
lymphnode_df["pt_id"] = lymphnode_df['Patient'].str[:-1]

for i in [2, 5, 10]:

    baseline = (
        lymphnode_df[lymphnode_df["CT#"] == 0][["pt_id", f"V{i}.0 dosevol"]]
        .rename(columns={f"V{i}.0 dosevol": f"V{i}_base"})
    )

    lymphnode_df = lymphnode_df.merge(baseline, on="pt_id", how="left")

    lymphnode_df[f"V{i}_delta"] = (
        lymphnode_df[f"V{i}.0 dosevol"] - lymphnode_df[f"V{i}_base"]
    )
print(lymphnode_df.head(20))

for i in [2,5,10]:
    plt.figure()
    valid_pts = lymphnode_df.groupby("pt_id")[f"V{i}.0 dosevol"].max() > 0
    valid_pts = valid_pts[valid_pts].index

    lymphnode_df = lymphnode_df[lymphnode_df["pt_id"].isin(valid_pts)]

    for pt, group in lymphnode_df.groupby("pt_id"):
        group = group.sort_values('CT#')
        plt.plot(group["CT#"], group[f"V{i}_delta"],alpha=0.2,color='black')

    std_df = (
        lymphnode_df
        .groupby("CT#")[f"V{i}_delta"]
        .std()
        .reset_index()
    )
    plt.plot([],[],color='black', alpha=0.2, label='Patients')
    plt.plot(std_df["CT#"], std_df[f"V{i}_delta"], linewidth=4,color='purple',label='Standard Deviation')
    plt.xlabel('CBCT#')
    plt.ylabel(fr'$\Delta$ V{i} (cc)')
    plt.title(f'Change in Lymphnode V{i} Dosevol From Baseline Over Each CT')
    plt.legend()
    
    filename = f"lymphnode_study/v{i}_delta.png"
    plt.savefig(filename)
    print(f"saved {filename}")
    
    plt.show()
