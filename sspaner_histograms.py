from pathlib import Path
import pandas as pd
import numpy as np

pat_data_3 = Path("./pat_data_3")

dfs = []
for folder in pat_data_3.iterdir():
    if folder.is_dir():
        for file in folder.glob("*.csv"):
            df = pd.read_csv(file)
            dfs.append(df)
all_data_df = pd.concat(dfs, ignore_index=True)

organ_name_dict = {"Aorta_KW":"Aorta", "BronchialTree_NoGTV":"BronchialTree", "BronchialTree_Prox":"BronchialTree","BronchialTree_Prox_KW":"BronchialTree", "A_Pulmonary":"PulmonaryArtery", "ChestWal":"CW", "ChestWall":"CW", "ChestWall_L":"CW", "ChestWall_New":"CW", "ChestWall_R":"CW", "Chestwall":"CW","Heart_KW":"Heart","LN-EContour":"LN", "LN-Econtour":"LN", "LN-Econtour-KW":"LN","Lung-ITV":"Lungs", "Lungs-ITV":"Lungs", "Lymph Node":"LN", "Lymph Node-Atlas":"LN", "LymphNode - Econtour":"LN", "LymphNode Atlas":"LN","LymphNode-ATlas":"LN","LymphNode-Atlas":"LN", "LymphNode-Econtour":"LN", "LymphNodeAtlas":"LN","LymphNode_Atlas":"LN","Lymphnode-Atlas":"LN","PA":"PulmonaryArtery","PA_KW":"PulmonaryArtery","PBT":"BronchialTree", "Prox Bronchial Tree":"BronchialTree", "ProximalBronchial_Tree":"BronchialTree","Pulm Art":"PulmonaryArtery","Pulm Artery":"PulmonaryArtery","PulmArt":"PulmonaryArtery","PulmArtery":"PulmonaryArtery","Pulm_Art":"PulmonaryArtery","Pulmonary Artery":"PulmonaryArtery","PulmonaryArteries":"PulmonaryArtery","Pulmonary_A":"PulmonaryArtery","Pulmonary_Artery":"PulmonaryArtery","S_Venacava_V":"SVC","Sup Vena Cava":"SVC","SuperiorVenaCava":"SVC","T Spine":"TSpine","T spine":"TSpine","Thoracic Spine":"TSpine","Thoracic Vertebrae":"TSpine","Thoracic spine":"TSpine","ThoracicSpine":"TSpine","ThoracicSpine dl":"TSpine","ThoracicSpine_KW":"TSpine","Thoracic_Spine":"TSpine","Thoracic_spine":"TSpine","ThoracicSpine":"TSpine","TotalLung-ITV":"Lungs","Tspine":"TSpine","Tspine_vertebral bodies":"TSpine","VC_KW":"VC","V_Cava":"VC","V_CavaSuperior":"SVC","V_Cava_Inf":"IVC","V_Cava_Sup":"SVC","Vena Cava":"VC","VenaCava":"VC","VenaCava Sup":"SVC","VenaCavaSuperior":"SVC","heart":"Heart","pulmonary artery":"PulmonaryArtery","thoracic spine":"TSpine","ThorasicSpine":"TSpine"}

all_data_df["Organ_Clean"] = all_data_df["Organ"].replace(organ_name_dict)
print(all_data_df.head(50))
    
