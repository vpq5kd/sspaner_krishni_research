from pd3_template import all_data_df as df
import seaborn as sns
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

numeric_columns = df.select_dtypes(include=["number"]).columns.drop(["CT#","Arm","arm"])

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

    "Arm ": "arm"
}


for column in numeric_columns:
    plt.figure()
    sns.violinplot(data=df, x="Organ_Clean", y=column, hue='Organ_Clean',legend=False,palette="spring")
    plt.xticks(rotation=60)
    plt.title(f"{column} Distribution for Each Organ".title())
    plt.ylabel(f"{column}")
    plt.xlabel("Organ")
    plt.tight_layout()
    
    filename = f"violin_plots/{column_filename_dict[column]}_vp.png"
    plt.savefig(filename)
    plt.close()
    print(f"Saved {filename}")
