import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from pd3_template import all_data_df

plt.figure()
all_data_df["Dose_Type"] = all_data_df["CT#"].apply(lambda x: "Planned" if x == 0 else "Delivered")
columns = ["V2.0 dosevol", "V5.0 dosevol", "V2.0 dosevol/volume", "V5.0 dosevol/volume"]
file_names_dict = {"V2.0 dosevol":"V2D", "V5.0 dosevol":"V5D","V2.0 dosevol/volume":"V2DV","V5.0 dosevol/volume":"V5DV"}
final_super_folder = "organ_hists/dosevol"
for (organ,arm), df_organ in all_data_df.groupby(["Organ_Clean","arm"]):
    for column in columns:
        try:

            try:
                Path(f"{final_super_folder}/{organ}").mkdir()
                print(f"Created {final_super_folder}/{organ}")
            except FileExistsError:
                print(f"{final_super_folder}/{organ} already exists.")
                pass
            
            planned_data = df_organ.loc[df_organ["Dose_Type"] == "Planned", column].dropna()
            delivered_data = df_organ.loc[df_organ["Dose_Type"] == "Delivered", column].dropna()
            data = df_organ[column].dropna()

            fig, ax = plt.subplots()

            ax.hist(planned_data, histtype='step', edgecolor='black', label='Planned')
            ax.hist(delivered_data, histtype='step', edgecolor='red', label='Delivered')

            mean = np.mean(data)
            median = np.median(data)
            std = np.std(data)
            min_val = np.min(data)
            max_val = np.max(data)
            counts = len(data)

            stats_text = (
                f"Entries = {counts}\n"
                f"Mean = {mean:.4f}\n"
                f"Median = {median:.4f}\n"
                f"Std Dev = {std:.4f}\n"
                f"Min = {min_val:.4f}\n"
                f"Max = {max_val:.4f}"
            )

            ax.text(
                0.98, 0.98,
                stats_text,
                transform=ax.transAxes,
                fontsize=10,
                verticalalignment='top',
                horizontalalignment='right',
                bbox=dict(
                    boxstyle='round',
                    facecolor='white',
                    alpha=0.8,
                    edgecolor='black'
                )
            )

            ax.set_xlabel(column)
            ax.set_ylabel("Counts")
            ax.set_title(f"Organ: {organ} | Arm: {arm}")
           
            ax.legend()
            filename=f"{final_super_folder}/{organ}/{organ}_{arm}_{file_names_dict[column]}.png"
            plt.savefig(filename)
            plt.close()
            print(f"Saved {filename}")

        except KeyError:
            continue
