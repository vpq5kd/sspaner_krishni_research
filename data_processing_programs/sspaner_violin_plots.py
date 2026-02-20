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

for column in numeric_columns:
    plt.figure()
    sns.violinplot(data=df, x="Organ_Clean", y=column,  palette="spring")
    plt.xticks(rotation=60)
    plt.title(f"{column} Distribution for Each Organ".title())
    plt.ylabel(f"{column}")
    plt.xlabel("Organ")
    plt.tight_layout()
    
    filename = f"violin_plots/{column}_vp.png"
    plt.savefig(filename)
    print(f"Saved {filename}")

