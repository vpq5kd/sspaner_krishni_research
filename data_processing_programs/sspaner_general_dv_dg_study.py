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
    "Max1_Dose"
]

df = all_data_df[cols].copy()
df["pt_id"] = df["Patient"].str[:-1]

os.makedirs("organ_study", exist_ok=True)

organs = sorted(df["Organ_Clean"].dropna().unique())

for organ in organs:
    organ_df = df[df["Organ_Clean"] == organ].copy()

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
        plot_df = plot_df.dropna(
            subset=[
                "Max_sqrt(grad(Dose)*Dose)_1",
                "Max1_Dose",
                f"V{i}_delta"
            ]
        )

        x = plot_df["Max_sqrt(grad(Dose)*Dose)_1"].to_numpy()
        x = x**2 / plot_df["Max1_Dose"].to_numpy()

        y = np.abs(plot_df[f"V{i}_delta"].to_numpy())

        plt.figure()
        plt.scatter(x, y, linewidth=4, color="purple", marker="+")
        plt.xlabel("Dose Gradient")
        plt.ylabel(fr"|$\Delta$ V{i} (cc)|")
        plt.title(
            f"Dose Gradient vs. Change in {organ} V{i} Dosevol From Baseline"
        )

        safe_organ = str(organ).replace("/", "_").replace(" ", "_")
        filename = f"organ_study/{safe_organ}_v{i}_delta_dosegrad.png"

        plt.savefig(filename, bbox_inches="tight")
        print(f"saved {filename}")
        plt.close()
