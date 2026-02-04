from pathlib import Path
import pandas as pd
import numpy as np
import ROOT
import sys

pat_data_3 = Path("./pat_data_3")
arm_relation_csv = Path("pat_data_3/arm_relation.csv")
arm_relation_df = pd.read_csv(arm_relation_csv)
arm_relation_df = arm_relation_df[["patient","arm"]]

dfs = []
for folder in pat_data_3.iterdir():
    if folder.is_dir():
        folder_name = folder.name
        arm = arm_relation_df.loc[arm_relation_df["patient"]==folder_name, "arm"].iloc[0]
        for file in folder.glob("*.csv"):
            df = pd.read_csv(file)
            df["arm"] = arm
            dfs.append(df)
all_data_df = pd.concat(dfs, ignore_index=True)

organ_name_dict = {"Aorta_KW":"Aorta", "BronchialTree_NoGTV":"BronchialTree", "BronchialTree_Prox":"BronchialTree","BronchialTree_Prox_KW":"BronchialTree", "A_Pulmonary":"PulmonaryArtery", "ChestWal":"CW", "ChestWall":"CW", "ChestWall_L":"CW", "ChestWall_New":"CW", "ChestWall_R":"CW", "Chestwall":"CW","Heart_KW":"Heart","LN-EContour":"LN", "LN-Econtour":"LN", "LN-Econtour-KW":"LN","Lung-ITV":"Lungs", "Lungs-ITV":"Lungs", "Lymph Node":"LN", "Lymph Node-Atlas":"LN", "LymphNode - Econtour":"LN", "LymphNode Atlas":"LN","LymphNode-ATlas":"LN","LymphNode-Atlas":"LN", "LymphNode-Econtour":"LN", "LymphNodeAtlas":"LN","LymphNode_Atlas":"LN","Lymphnode-Atlas":"LN","PA":"PulmonaryArtery","PA_KW":"PulmonaryArtery","PBT":"BronchialTree", "Prox Bronchial Tree":"BronchialTree", "ProximalBronchial_Tree":"BronchialTree","Pulm Art":"PulmonaryArtery","Pulm Artery":"PulmonaryArtery","PulmArt":"PulmonaryArtery","PulmArtery":"PulmonaryArtery","Pulm_Art":"PulmonaryArtery","Pulmonary Artery":"PulmonaryArtery","PulmonaryArteries":"PulmonaryArtery","Pulmonary_A":"PulmonaryArtery","Pulmonary_Artery":"PulmonaryArtery","S_Venacava_V":"VC","Sup Vena Cava":"VC","SuperiorVenaCava":"VC","T Spine":"TSpine","T spine":"TSpine","Thoracic Spine":"TSpine","Thoracic Vertebrae":"TSpine","Thoracic spine":"TSpine","ThoracicSpine":"TSpine","ThoracicSpine dl":"TSpine","ThoracicSpine_KW":"TSpine","Thoracic_Spine":"TSpine","Thoracic_spine":"TSpine","ThoracicSpine":"TSpine","TotalLung-ITV":"Lungs","Tspine":"TSpine","Tspine_vertebral bodies":"TSpine","VC_KW":"VC","V_Cava":"VC","V_CavaSuperior":"VC","V_Cava_Inf":"IVC","V_Cava_Sup":"VC","Vena Cava":"VC","VenaCava":"VC","VenaCava Sup":"VC","VenaCavaSuperior":"VC","heart":"Heart","pulmonary artery":"PulmonaryArtery","thoracic spine":"TSpine","ThorasicSpine":"TSpine", "Pulmonary Vessels":"PulmonaryArtery","SVC":"VC"}

removed_vals = ["IVC", "SpinalCord", "ITV"]
all_data_df["Organ_Clean"] = all_data_df["Organ"].replace(organ_name_dict)
all_data_df = all_data_df[~all_data_df["Organ_Clean"].isin(removed_vals)]
all_data_df = all_data_df[all_data_df["Unnamed: 0"] != 0] #elim control ct for analysis"
all_data_df = all_data_df.rename(columns={"Unnamed: 0":"CT#"})


fit_function = ROOT.TF1("exp1","[0] * TMath::Exp(-[1]*(1-x))",0,1)
fit_function.SetParNames("Norm", "Lambda")
fit_function.SetParameters(300,5)

full_hist = ROOT.TH1F("h",f"Total Fraction Overlap",25,0,1)
full_hist_arm1 = ROOT.TH1F("full hist arm 1",f"Total Fraction Overlap",25,0,1)
full_hist_arm2 = ROOT.TH1F("full hist arm 2",f"Total Fraction Overlap",25,0,1)
hists = []
organs = []
for (organ,arm), df_organ in all_data_df.groupby(["Organ_Clean","arm"]):
    hist = ROOT.TH1F(f"{organ} arm: {arm}",f"{organ} arm:{arm} Fraction Overlap Hist;Fraction Overlap;Counts", 25, 0, 1)
    for val in df_organ["FractionOverlap"]:
        if val != "NaN":
            hist.Fill(val)
            full_hist.Fill(val)

            if arm == 1:
                full_hist_arm1.Fill(val)
            else:
                full_hist_arm2.Fill(val)

    print(f'{organ} arm:{arm} fit results')
    fit_result = hist.Fit(fit_function, "RS")
    try: 
        chi2 = fit_result.Chi2()
        ndf = fit_result.Ndf()
        rchi2 = chi2/ndf
        hist.SetTitle(f"{organ} arm:{arm} Fraction Overlap Hist. Reduced Chi2: {rchi2};Fraction Overlap; Counts")
    except:
       print("fit not working for {organ}...")
       continue
    hists.append(hist)
    organs.append([organ,arm])

print('all data fit result')

full_hist_fit_result = full_hist.Fit(fit_function, "RS")

chi2 = full_hist_fit_result.Chi2()
ndf = full_hist_fit_result.Ndf()
rchi2 = chi2/ndf

full_hist.SetTitle(f"Fraction Overlap Hist for all Organs. Reduced Chi2: {rchi2};Fraction Overlap; Counts")
hists.append(full_hist)
organs.append(["Full_Hist",0])


full_hist_arms = [full_hist_arm1, full_hist_arm2]
arm_full_hist_arms = 1
for hist in full_hist_arms:

    print(f'Full hist arm: {arm_full_hist_arms} fit result')
    full_hist_fit_result = hist.Fit(fit_function, "RS")

    chi2 = full_hist_fit_result.Chi2()
    ndf = full_hist_fit_result.Ndf()
    rchi2 = chi2/ndf

    hist.SetTitle(f"Fraction Overlap Hist for all Organs in Arm {arm_full_hist_arms}. Reduced Chi2: {rchi2};Fraction Overlap; Counts")
    hists.append(hist)
    organs.append(["Full Hist",arm_full_hist_arms])
    arm_full_hist_arms+=1



c = ROOT.TCanvas("c","canvas", 800,600)
organ_index = 0
for hist in hists:
    organ = organs[organ_index][0]
    arm = organs[organ_index][1]
    hist.Draw()
    c.Update()
    c.SaveAs(f"organ_hists/by_arm/{organ}_arm{arm}_hist.png")
    organ_index+=1

input("Please press enter to exit...")
