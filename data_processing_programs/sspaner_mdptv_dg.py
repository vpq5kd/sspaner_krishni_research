import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pd3_template import all_data_df

cols = ['DminFromPTV (mm)', 'arm', 'Max_sqrt(grad(Dose)*Dose)_1', 'Organ_Clean', 'Max1_Dose']

df = all_data_df[cols].copy()


for (organ, arm), df_ao in df.groupby(['Organ_Clean', 'arm']):
    
    x = df_ao['DminFromPTV (mm)'].to_numpy()
    y = df_ao["Max_sqrt(grad(Dose)*Dose)_1"].to_numpy()
    y = x**2 / df_ao["Max1_Dose"].to_numpy()
    plt.figure()
    plt.scatter(x,y, color='black', marker='+')
    plt.xlabel('Minimum Distance from PTV')
    plt.ylabel('Dose Gradient')
    plt.title(f'Dose Gradient vs. Minimum Distance from PTV for {organ} in arm {arm}')
    filename = f'mdptv_dg_study/{organ}_{arm}.png'
    plt.savefig(filename)
    print(f'Saved {filename}.')
    plt.close() 
