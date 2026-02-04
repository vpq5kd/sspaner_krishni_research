from pathlib import Path
import pandas as pd
import numpy as np
import ROOT
import sys

import sspaner_pat_data_3_processing_template as template

all_data_df = template.all_data_df

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
