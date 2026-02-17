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

plt.figure()
sns.violinplot(data=df, x="Organ_Clean", y="MeanDose",palette="spring")
plt.xticks(rotation=60)
plt.title("Mean Dose Distribution for Each Organ".title())
plt.ylabel("Mean Dose (Gy)")
plt.xlabel("Organ")
plt.tight_layout()
plt.savefig("violin_plots/mean_dose_vp.png")
plt.show()
