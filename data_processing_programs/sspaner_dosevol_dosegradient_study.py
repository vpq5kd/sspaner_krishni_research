import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pd3_template import all_data_df

lymphnode_df = all_data_df[all_data_df["Organ_Clean"] == "LN"]
cols = ['V2.0 dosevol','V5.0 dosevol', 'V10.0 dosevol', 'Patient', 'CT#', 'TotalVolume (cm^3)', 'RTOG', 'Max_sqrt(grad(Dose)*Dose)_1', 'Max1_Dose']

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

   
    x  = lymphnode_df["Max_sqrt(grad(Dose)*Dose)_1"].to_numpy()
    x = x**2
    x = x/(lymphnode_df['Max1_Dose'].to_numpy())
 
    plt.scatter(x, np.abs(lymphnode_df[f"V{i}_delta"]), linewidth=4,color='purple',marker='+')
    plt.xlabel('Dose Gradient')
    plt.ylabel(fr'|$\Delta$ V{i} (cc)|')
    plt.title(f'Dose Gradient vs. Change in Lymphnode V{i} Dosevol From Baseline')
    
    filename = f"lymphnode_study/v{i}_delta_dosegrad.png"

    plt.savefig(filename)
    print(f"saved {filename}")
    
    plt.show()
