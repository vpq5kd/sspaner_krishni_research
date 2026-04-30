import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pd3_template import all_data_df

cols = [
    "Patient",
    "Organ_Clean",
    "FractionOverlap",
    "arm"
]

df = all_data_df[cols].copy()
df["pt_id"] = df["Patient"].str[:-1]

plot_df = df
plt.figure(figsize=(14, 6))

sns.boxplot(
    data=plot_df,
    x="Organ_Clean",
    y="FractionOverlap",
    showfliers=False,
    linecolor='mediumvioletred',
    color=".8"
)

plt.xticks(rotation=60, ha="right")
plt.ylabel("Fraction Overlap")
plt.xlabel("Organ")
plt.tight_layout()

filename = "figure5.png"
plt.savefig(filename)
plt.show()

