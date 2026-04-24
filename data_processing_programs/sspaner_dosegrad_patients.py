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

df["dosegrad"] = (
    df["Max_sqrt(grad(Dose)*Dose)_1"]**2
    / df["Max1_Dose"]
)

high = df[df["dosegrad"] >= 20]

print(high[[
    "pt_id",
    "Patient",
    "Organ_Clean",
    "CT#",
    "arm",
    "Max_sqrt(grad(Dose)*Dose)_1",
    "Max1_Dose",
    "dosegrad"
]])        
