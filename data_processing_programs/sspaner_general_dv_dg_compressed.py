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


markers = ['o', 's', '^', 'D', 'v', 'P', 'X', '*', '<', '>', 'h', 'H']

organ_markers = {
    organ: markers[i % len(markers)]
    for i, organ in enumerate(organs)
}

for i in [2, 5, 10]:
    plt.figure()
    for organ in organs:

        organ_df = df[df["Organ_Clean"] == organ].copy()
        baseline = (
            organ_df[organ_df["CT#"] == 0][["pt_id", f"V{i}.0 dosevol"]]
            .drop_duplicates(subset=["pt_id"])
            .rename(columns={f"V{i}.0 dosevol": f"V{i}_base"})
        )

        organ_df = organ_df.merge(baseline, on="pt_id", how="left")

        organ_df[f"V{i}_delta"] = (
            organ_df[f"V{i}.0 dosevol"] - organ_df[f"V{i}_base"]
        )

        valid_pts = organ_df.groupby("pt_id")[f"V{i}.0 dosevol"].max() > 0
        valid_pts = valid_pts[valid_pts].index

        plot_df = organ_df[organ_df["pt_id"].isin(valid_pts)].copy()
        #plot_df = plot_df.dropna(
         #   subset=[
          #      "Max_sqrt(grad(Dose)*Dose)_1",
           #     "Max1_Dose",
            #    f"V{i}_delta"
            #]
        #)

        x1 = plot_df[plot_df["arm"]==1]["Max_sqrt(grad(Dose)*Dose)_1"].to_numpy()
        x2 = plot_df[plot_df["arm"]==2]["Max_sqrt(grad(Dose)*Dose)_1"].to_numpy()
        x1 = x1**2 / plot_df[plot_df["arm"]==1]["Max1_Dose"].to_numpy()
        x2 = x2**2/ plot_df[plot_df["arm"]==2]["Max1_Dose"].to_numpy() 
        y1 =plot_df[plot_df["arm"]==1][f"V{i}_delta"].to_numpy()

        y2 =plot_df[plot_df["arm"]==2][f"V{i}_delta"].to_numpy()
        plt.scatter(x1, y1, linewidth=4, color="blue", marker=organ_markers[organ],label="arm 1")
        plt.scatter(x2, y2, linewidth=4, color="mediumvioletred", marker=organ_markers[organ], label='arm 2')
    #plt.legend()
    plt.xlabel("Dose Gradient")
    plt.ylabel(fr"$\Delta$ V{i} (cc)")
    plt.title(
        f"Change in {organ} V{i} Dosevol From Baseline vs. Dose Gradient"
    )
    #safe_organ = str(organ).replace("/", "_").replace(" ", "_")
    #filename = f"organ_study/{safe_organ}_v{i}_delta_dosegrad.png"

    #plt.savefig(filename, bbox_inches="tight")
    plt.show()
    print(f"saved {filename}")
    plt.close()
