from pathlib import Path
import pandas as pd
import numpy as np
import sys

pat_data_3 = Path("./pat_data_3")
arm_relation_csv = Path("pat_data_3/arm_relation.csv")
arm_relation_df = pd.read_csv(arm_relation_csv)
arm_relation_df = arm_relation_df[["patient","arm","RTOG"]]

dfs = []
for folder in pat_data_3.iterdir():
    if folder.is_dir():
        folder_name = folder.name
        arm = arm_relation_df.loc[arm_relation_df["patient"]==folder_name, "arm"].iloc[0]
        RTOG = arm_relation_df.loc[arm_relation_df["patient"]==folder_name, "RTOG"].iloc[0]
        for file in folder.glob("*.csv"):
            df = pd.read_csv(file)
            df["arm"] = arm
            df["RTOG"] = RTOG
            dfs.append(df)
all_data_df = pd.concat(dfs, ignore_index=True)

organ_name_dict = {"Aorta_KW":"Aorta", "BronchialTree_NoGTV":"BronchialTree", "BronchialTree_Prox":"BronchialTree","BronchialTree_Prox_KW":"BronchialTree", "A_Pulmonary":"PulmonaryArtery", "ChestWal":"CW", "ChestWall":"CW", "ChestWall_L":"CW", "ChestWall_New":"CW", "ChestWall_R":"CW", "Chestwall":"CW","Heart_KW":"Heart","LN-EContour":"LN", "LN-Econtour":"LN", "LN-Econtour-KW":"LN","Lung-ITV":"Lungs", "Lungs-ITV":"Lungs", "Lymph Node":"LN", "Lymph Node-Atlas":"LN", "LymphNode - Econtour":"LN", "LymphNode Atlas":"LN","LymphNode-ATlas":"LN","LymphNode-Atlas":"LN", "LymphNode-Econtour":"LN", "LymphNodeAtlas":"LN","LymphNode_Atlas":"LN","Lymphnode-Atlas":"LN","PA":"PulmonaryArtery","PA_KW":"PulmonaryArtery","PBT":"BronchialTree", "Prox Bronchial Tree":"BronchialTree", "ProximalBronchial_Tree":"BronchialTree","Pulm Art":"PulmonaryArtery","Pulm Artery":"PulmonaryArtery","PulmArt":"PulmonaryArtery","PulmArtery":"PulmonaryArtery","Pulm_Art":"PulmonaryArtery","Pulmonary Artery":"PulmonaryArtery","PulmonaryArteries":"PulmonaryArtery","Pulmonary_A":"PulmonaryArtery","Pulmonary_Artery":"PulmonaryArtery","S_Venacava_V":"VC","Sup Vena Cava":"VC","SuperiorVenaCava":"VC","T Spine":"TSpine","T spine":"TSpine","Thoracic Spine":"TSpine","Thoracic Vertebrae":"TSpine","Thoracic spine":"TSpine","ThoracicSpine":"TSpine","ThoracicSpine dl":"TSpine","ThoracicSpine_KW":"TSpine","Thoracic_Spine":"TSpine","Thoracic_spine":"TSpine","ThoracicSpine":"TSpine","TotalLung-ITV":"Lungs","Tspine":"TSpine","Tspine_vertebral bodies":"TSpine","VC_KW":"VC","V_Cava":"VC","V_CavaSuperior":"VC","V_Cava_Inf":"IVC","V_Cava_Sup":"VC","Vena Cava":"VC","VenaCava":"VC","VenaCava Sup":"VC","VenaCavaSuperior":"VC","heart":"Heart","pulmonary artery":"PulmonaryArtery","thoracic spine":"TSpine","ThorasicSpine":"TSpine", "Pulmonary Vessels":"PulmonaryArtery","SVC":"VC"}

removed_vals = ["IVC", "SpinalCord", "ITV","Bronchus"]
all_data_df["Organ_Clean"] = all_data_df["Organ"].replace(organ_name_dict)
all_data_df = all_data_df[~all_data_df["Organ_Clean"].isin(removed_vals)]
#all_data_df = all_data_df[all_data_df["Unnamed: 0"] != 0] #elim control ct for analysis"
all_data_df = all_data_df.rename(columns={"Unnamed: 0":"CT#"})

