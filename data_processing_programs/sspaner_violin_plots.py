from pd3_template import all_data_df as df
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
import os
import seaborn as sns
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

df["Organ_Clean"] = (
    df["Organ_Clean"]
        .str.strip()
        .str.lower()
        .replace({
            "tspine": "thoracic spine",
            "pulmonaryartery": "pulmonary artery",
            "vc": "vena cava",
            "bronchialtree": "bronchial tree",
            "spinalcanal": "spinal canal",
            "cw": "chest wall",
            "ln": "lymph node"
        })
        .str.title()
)

numeric_columns = df.select_dtypes(include=["number"]).columns.drop(["CT#","Arm","Arm ","arm", "RTOG"])

column_filename_dict = {
    "MinDose": "min_dose",
    "MaxDose": "max_dose",
    "MeanDose": "mean_dose",
    "TotalVolume (cm^3)": "total_volume_cm3",
    "IntegralDose": "integral_dose",
    "VolumeOverlap": "volume_overlap",
    "FractionOverlap": "fraction_overlap",
    "DminFromPTV (mm)": "dmin_from_ptv_mm",
    "CM Distance (mm)": "cm_distance_mm",

    "Max_sqrt(grad(Dose)*Dose)_1": "max_grad_dose_1",
    "Max1_Dose": "max1_dose",
    "Max_sqrt(grad(Dose)*Dose)_2": "max_grad_dose_2",
    "Max2_Dose": "max2_dose",
    "Max_sqrt(grad(Dose)*Dose)_3": "max_grad_dose_3",
    "Max3_Dose": "max3_dose",
    "Max_sqrt(grad(Dose)*Dose)_4": "max_grad_dose_4",
    "Max4_Dose": "max4_dose",
    "Max_sqrt(grad(Dose)*Dose)_5": "max_grad_dose_5",
    "Max5_Dose": "max5_dose",

    "V1.0 dosevol": "v1_dosevol",
    "V1.0 dosevol/volume": "v1_dosevol_per_volume",
    "V2.0 dosevol": "v2_dosevol",
    "V2.0 dosevol/volume": "v2_dosevol_per_volume",
    "V5.0 dosevol": "v5_dosevol",
    "V5.0 dosevol/volume": "v5_dosevol_per_volume",
    "V10.0 dosevol": "v10_dosevol",
    "V10.0 dosevol/volume": "v10_dosevol_per_volume",
    "V15.0 dosevol": "v15_dosevol",
    "V15.0 dosevol/volume": "v15_dosevol_per_volume",
    "V20.0 dosevol": "v20_dosevol",
    "V20.0 dosevol/volume": "v20_dosevol_per_volume",

    "V50.0 dosevol": "v50_dosevol",
    "V50.0 dosevol/volume": "v50_dosevol_per_volume",
    "V55.0 dosevol": "v55_dosevol",
    "V55.0 dosevol/volume": "v55_dosevol_per_volume",
    "V60.0 dosevol": "v60_dosevol",
    "V60.0 dosevol/volume": "v60_dosevol_per_volume",
    "V65.0 dosevol": "v65_dosevol",
    "V65.0 dosevol/volume": "v65_dosevol_per_volume",
    "V70.0 dosevol": "v70_dosevol",
    "V70.0 dosevol/volume": "v70_dosevol_per_volume",
    "V75.0 dosevol": "v75_dosevol",
    "V75.0 dosevol/volume": "v75_dosevol_per_volume",

}


column_title_dict = {
    "MinDose": "Minimum Dose",
    "MaxDose": "Maximum Dose",
    "MeanDose": "Mean Dose",
    "TotalVolume (cm^3)": "Total Volume",
    "IntegralDose": "Integral Dose",
    "VolumeOverlap": "Volume Overlap",
    "FractionOverlap": "Fraction Overlap",
    "DminFromPTV (mm)": "Minimum Distance from PTV",
    "CM Distance (mm)": "Center of Mass Distance",

    "Max_sqrt(grad(Dose)*Dose)_1": "Max sqrt(∇Dose · Dose) (1)",
    "Max1_Dose": "Maximum Dose (1)",
    "Max_sqrt(grad(Dose)*Dose)_2": "Max sqrt(∇Dose · Dose) (2)",
    "Max2_Dose": "Maximum Dose (2)",
    "Max_sqrt(grad(Dose)*Dose)_3": "Max sqrt(∇Dose · Dose) (3)",
    "Max3_Dose": "Maximum Dose (3)",
    "Max_sqrt(grad(Dose)*Dose)_4": "Max sqrt(∇Dose · Dose) (4)",
    "Max4_Dose": "Maximum Dose (4)",
    "Max_sqrt(grad(Dose)*Dose)_5": "Max sqrt(∇Dose · Dose) (5)",
    "Max5_Dose": "Maximum Dose (5)",

    "V1.0 dosevol": "V1 Dose Volume",
    "V1.0 dosevol/volume": "V1 Dose Volume Fraction",
    "V2.0 dosevol": "V2 Dose Volume",
    "V2.0 dosevol/volume": "V2 Dose Volume Fraction",
    "V5.0 dosevol": "V5 Dose Volume",
    "V5.0 dosevol/volume": "V5 Dose Volume Fraction",
    "V10.0 dosevol": "V10 Dose Volume",
    "V10.0 dosevol/volume": "V10 Dose Volume Fraction",
    "V15.0 dosevol": "V15 Dose Volume",
    "V15.0 dosevol/volume": "V15 Dose Volume Fraction",
    "V20.0 dosevol": "V20 Dose Volume",
    "V20.0 dosevol/volume": "V20 Dose Volume Fraction",

    "V50.0 dosevol": "V50 Dose Volume",
    "V50.0 dosevol/volume": "V50 Dose Volume Fraction",
    "V55.0 dosevol": "V55 Dose Volume",
    "V55.0 dosevol/volume": "V55 Dose Volume Fraction",
    "V60.0 dosevol": "V60 Dose Volume",
    "V60.0 dosevol/volume": "V60 Dose Volume Fraction",
    "V65.0 dosevol": "V65 Dose Volume",
    "V65.0 dosevol/volume": "V65 Dose Volume Fraction",
    "V70.0 dosevol": "V70 Dose Volume",
    "V70.0 dosevol/volume": "V70 Dose Volume Fraction",
    "V75.0 dosevol": "V75 Dose Volume",
    "V75.0 dosevol/volume": "V75 Dose Volume Fraction",
}

column_ylabel_dict = {
    "MinDose": "Dose (Gy)",
    "MaxDose": "Dose (Gy)",
    "MeanDose": "Dose (Gy)",
    "TotalVolume (cm^3)": "Volume (cm³)",
    "IntegralDose": "Integral Dose (Gy·cm³)",
    "VolumeOverlap": "Volume (cm³)",
    "FractionOverlap": "Fraction",
    "DminFromPTV (mm)": "Distance (mm)",
    "CM Distance (mm)": "Distance (mm)",

    "Max_sqrt(grad(Dose)*Dose)_1": "sqrt(∇Dose · Dose)",
    "Max1_Dose": "Dose (Gy)",
    "Max_sqrt(grad(Dose)*Dose)_2": "sqrt(∇Dose · Dose)",
    "Max2_Dose": "Dose (Gy)",
    "Max_sqrt(grad(Dose)*Dose)_3": "sqrt(∇Dose · Dose)",
    "Max3_Dose": "Dose (Gy)",
    "Max_sqrt(grad(Dose)*Dose)_4": "sqrt(∇Dose · Dose)",
    "Max4_Dose": "Dose (Gy)",
    "Max_sqrt(grad(Dose)*Dose)_5": "sqrt(∇Dose · Dose)",
    "Max5_Dose": "Dose (Gy)",

    "V1.0 dosevol": "Volume (cm³)",
    "V1.0 dosevol/volume": "Fraction",
    "V2.0 dosevol": "Volume (cm³)",
    "V2.0 dosevol/volume": "Fraction",
    "V5.0 dosevol": "Volume (cm³)",
    "V5.0 dosevol/volume": "Fraction",
    "V10.0 dosevol": "Volume (cm³)",
    "V10.0 dosevol/volume": "Fraction",
    "V15.0 dosevol": "Volume (cm³)",
    "V15.0 dosevol/volume": "Fraction",
    "V20.0 dosevol": "Volume (cm³)",
    "V20.0 dosevol/volume": "Fraction",

    "V50.0 dosevol": "Volume (cm³)",
    "V50.0 dosevol/volume": "Fraction",
    "V55.0 dosevol": "Volume (cm³)",
    "V55.0 dosevol/volume": "Fraction",
    "V60.0 dosevol": "Volume (cm³)",
    "V60.0 dosevol/volume": "Fraction",
    "V65.0 dosevol": "Volume (cm³)",
    "V65.0 dosevol/volume": "Fraction",
    "V70.0 dosevol": "Volume (cm³)",
    "V70.0 dosevol/volume": "Fraction",
    "V75.0 dosevol": "Volume (cm³)",
    "V75.0 dosevol/volume": "Fraction",
}

df["CT_Group"] = df["CT#"].apply(lambda x: "Planned" if x == 0 else "Delivered")


def make_violin_plot(column):
    plt.figure(figsize=(18,8))

    plot_df = df

    if column == 'DminFromPTV (mm)':
        plot_df = df[df["Organ_Clean"] != "Lungs-Itv"]

    sns.violinplot(
        data=plot_df,
        x="Organ_Clean",
        y=column,
        hue="CT_Group",
        palette="spring",
        density_norm="width"
    )

    plt.xticks(rotation=60)
    plt.title(f"{column_title_dict[column]} Distribution for Each Organ")
    plt.ylabel(column_ylabel_dict[column])
    plt.xlabel("Organ")
    plt.tight_layout()

    filename = f"violin_plots/{column_filename_dict[column]}_vp.png"
    #plt.show()
    plt.savefig(filename)
    plt.close()

    return filename

def main():
    '''
    print(f"Processing data with {os.cpu_count()} cores.")
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        results = list(
            tqdm(
                executor.map(make_violin_plot, numeric_columns),
                total=len(numeric_columns)
            )
        )
    '''
    for column in numeric_columns:
        filename = make_violin_plot(column)
        print(f"saved {filename}")

if __name__ == "__main__":
    main()
