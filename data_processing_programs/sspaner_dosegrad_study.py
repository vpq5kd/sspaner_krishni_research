import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from pd3_template import all_data_df

plt.figure(figsize=(10,12))
for organ,organ_df in all_data_df.groupby("Organ_Clean"):
    for i in [2,5,10]:
        organ_df["pt_id"] = organ_df['Patient'].str[:-1]


        y = organ_df[f"V{i}.0 dosevol"]
        x = organ_df["Max_sqrt(grad(Dose)*Dose)_1"].to_numpy()

        x = x**2
        x = x/(organ_df['Max1_Dose'].to_numpy())

        plt.scatter(x,y,color='mediumvioletred',marker="+")
        plt.xlabel(r"$\frac{(Max\_sqrt(grad(Dose)*Dose)\_1)^2}{(Max1\_Dose)}$")
        plt.ylabel(f"V{i}.0 dosevol")
        plt.title(f"Max Gradient 1 vs. V{i}.0 Dosevol for {organ}")
        
        filename = f"dosegrad_study/{organ}_v{i}.png"
        plt.savefig(filename)
        
        print(f"saved {filename}")
