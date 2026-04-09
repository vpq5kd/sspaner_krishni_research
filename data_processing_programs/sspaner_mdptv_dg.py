import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pd3_template import all_data_df

cols = ['DminFromPTV (mm)', 'arm', 'Max_sqrt(grad(Dose)*Dose)_1', 'Organ_Clean', 'Max1_Dose']

df = all_data_df[cols].copy()


for organ, df_ao in df.groupby(['Organ_Clean']):
    
    x1 = df_ao[df_ao["arm"]==1]['DminFromPTV (mm)'].to_numpy()
    x2 = df_ao[df_ao["arm"]==2]['DminFromPTV (mm)'].to_numpy()

    y1 = df_ao[df_ao["arm"]==1]["Max_sqrt(grad(Dose)*Dose)_1"].to_numpy()
    y2 = df_ao[df_ao["arm"]==2]["Max_sqrt(grad(Dose)*Dose)_1"].to_numpy()
    
    
    y1 = y1**2 / df_ao[df_ao["arm"]==1]["Max1_Dose"].to_numpy()

    y2 = y2**2 / df_ao[df_ao["arm"]==2]["Max1_Dose"].to_numpy()

    
    plt.figure()
    plt.scatter(x1,y1, color='black', marker='+', label='arm 1')
    plt.scatter(x2,y2, color='magenta', marker='x',label='arm 2')
    plt.legend()
    plt.xlabel('Minimum Distance from PTV')
    plt.ylabel('Dose Gradient')
    plt.title(f'Dose Gradient vs. Minimum Distance from PTV for {organ[0]}')
    filename = f'mdptv_dg_study/{organ[0]}.png'
    plt.savefig(filename)
    print(f'Saved {filename}.')
    plt.close() 
