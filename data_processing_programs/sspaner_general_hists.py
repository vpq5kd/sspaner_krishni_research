import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from pd3_template import all_data_df

plt.figure()
all_data_df["Dose_Type"] = all_data_df["CT#"].apply(lambda x: "Planned" if x == 0 else "Delivered")
columns = ["V2.0 dosevol", "V5.0 dosevol", "V2.0 dosevol/volume", "V5.0 dosevol/volume", "V10.0 dosevol", "V10.0 dosevol/volume"]
file_names_dict = {"V2.0 dosevol":"V2D", "V5.0 dosevol":"V5D","V2.0 dosevol/volume":"V2DV","V5.0 dosevol/volume":"V5DV", "V10.0 dosevol":"V10D", "V10.0 dosevol/volume":"V10DV"}
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
            fig, ax = plt.subplots()

            ax.hist(planned_data, histtype='step', edgecolor='green', label='Planned',density=True)
            ax.hist(delivered_data, histtype='stepfilled', edgecolor='black', facecolor='pink', label='Delivered', density=True)
            
            ax.axvline(planned_data.mean(), color='grey', linestyle='--', label='Planned Mean', linewidth = 3)
            ax.axvline(delivered_data.mean(), color='black', linestyle='--', label='Delivered Mean', linewidth = 3)
            
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
                f"Max = {max_val:.4f}\n"
                f"M_Diff = {planned_data.mean() - delivered_data.mean()}"
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
            ax.set_ylabel("Normalized Counts")
            ax.set_title(f"Organ: {organ} | Arm: {arm}")
           
            ax.legend(loc='center right')
            filename=f"{final_super_folder}/{organ}/{organ}_{arm}_{file_names_dict[column]}.png"
            #plt.show()
            plt.savefig(filename)
            plt.close()
            print(f"Saved {filename}")

        except KeyError:
            continue
