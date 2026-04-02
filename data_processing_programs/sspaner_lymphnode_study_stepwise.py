import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pd3_template import all_data_df

lymphnode_df = all_data_df[all_data_df["Organ_Clean"] == "LN"].copy()

cols = [
    "V2.0 dosevol",
    "V5.0 dosevol",
    "V10.0 dosevol",
    "Patient",
    "CT#",
    "TotalVolume (cm^3)",
    "RTOG"
]

lymphnode_df = lymphnode_df[cols].copy()
lymphnode_df["pt_id"] = lymphnode_df["Patient"].str[:-1]

lymphnode_df = lymphnode_df.sort_values(["pt_id", "CT#"]).copy()

for i in [2, 5, 10]:
    lymphnode_df[f"V{i}_step_delta"] = (
        lymphnode_df
        .groupby("pt_id")[f"V{i}.0 dosevol"]
        .diff()
    )
print(lymphnode_df.head(20))

for i in [2, 5, 10]:
    plt.figure()

    valid_pts = lymphnode_df.groupby("pt_id")[f"V{i}.0 dosevol"].max() > 0
    valid_pts = valid_pts[valid_pts].index

    df_plot = lymphnode_df[lymphnode_df["pt_id"].isin(valid_pts)].copy()

    for pt, group in df_plot.groupby("pt_id"):
        group = group.sort_values("CT#")
        plt.plot(
            group["CT#"],
            group[f"V{i}_step_delta"],
            alpha=0.2,
            color="black"
        )

    mean_df = (
        df_plot
        .groupby("CT#")[f"V{i}_step_delta"]
        .std()
        .reset_index()
    )

    plt.plot([], [], color="black", alpha=0.2, label="Patients")
    plt.plot(
        mean_df["CT#"],
        mean_df[f"V{i}_step_delta"],
        linewidth=4,
        color="orange",
        label="Standard Deviation"
    )

    plt.xlabel("CBCT#")
    plt.xticks(range(6))
    plt.xlim(1,5)
    plt.ylabel(fr"$\Delta$ V{i} step (cc)")
    plt.title(f"Stepwise Change in Lymphnode V{i} Dosevol Over Each CT")
    plt.legend()

    filename = f"lymphnode_study/v{i}_step_delta.png"
    plt.savefig(filename)
    print(f"saved {filename}")

    plt.show()
