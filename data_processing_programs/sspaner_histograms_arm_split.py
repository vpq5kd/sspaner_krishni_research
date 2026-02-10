from pathlib import Path
import pandas as pd
import numpy as np
import ROOT
import sys

import sspaner_pat_data_3_processing_template as template

import argparse

parser = argparse.ArgumentParser('Data Analysis of Fractional Volume Overlap')
parser.add_argument('--fitfunc',type=str,default='exponential', choices=['exponential','gausian'], help='fit function')
parser.add_argument('--showfit', type=str, default='yes', choices=['yes','no'], help='show fit on graph')
args = parser.parse_args()

all_data_df = template.all_data_df

exponential_fit_func = ROOT.TF1("exp1","[0] * TMath::Exp(-[1]*(1-x))",0,1)
exponential_fit_func.SetParNames("Norm", "Lambda")
exponential_fit_func.SetParameters(300,5)

fit_dict = {'gausian':'gaus','exponential':exponential_fit_func}
show_fit_dict = {'yes':'RS','no':'0RS'}
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
    fit_result = hist.Fit(fit_dict[args.fitfunc], show_fit_dict[args.showfit])
    try: 
        chi2 = fit_result.Chi2()
        ndf = fit_result.Ndf()
        rchi2 = chi2/ndf
        if args.showfit == 'yes':
            hist.SetTitle(f"{organ} | Arm: {arm} | Fractional Volume Overlap Distribution | Reduced Chi2: {rchi2};Fraction Overlap; Counts")
        else:
            hist.SetTitle(f"{organ} | Arm: {arm} | Fractional Volume Overlap Distribution;Fraction Overlap; Counts")
    except:
       print("fit not working for {organ}...")
       continue
    hists.append(hist)
    organs.append([organ,arm])

print('all data fit result')

full_hist_fit_result = full_hist.Fit(fit_dict[args.fitfunc], show_fit_dict[args.showfit])

chi2 = full_hist_fit_result.Chi2()
ndf = full_hist_fit_result.Ndf()
rchi2 = chi2/ndf
if args.showfit == 'yes':
    hist.SetTitle(f"{organ} | Arm: {arm} | Fractional Volume Overlap Distribution | Reduced Chi2: {rchi2};Fraction Overlap; Counts")
else:
    hist.SetTitle(f"{organ} | Arm: {arm} | Fractional Volume Overlap Distribution;Fraction Overlap; Counts")
hists.append(full_hist)
organs.append(["Full_Hist",0])


full_hist_arms = [full_hist_arm1, full_hist_arm2]
arm_full_hist_arms = 1
for hist in full_hist_arms:

    print(f'Full hist arm: {arm_full_hist_arms} fit result')
    full_hist_fit_result = hist.Fit(fit_dict[args.fitfunc], show_fit_dict[args.showfit])

    chi2 = full_hist_fit_result.Chi2()
    ndf = full_hist_fit_result.Ndf()
    rchi2 = chi2/ndf
if args.showfit == 'yes':
    hist.SetTitle(f"{organ} | Arm: {arm} | Fractional Volume Overlap Distribution | Reduced Chi2: {rchi2};Fraction Overlap; Counts")
else:
    hist.SetTitle(f"{organ} | Arm: {arm} | Fractional Volume Overlap Distribution;Fraction Overlap; Counts")
    hists.append(hist)
    organs.append(["Full Hist",arm_full_hist_arms])
    arm_full_hist_arms+=1



c = ROOT.TCanvas("c","canvas", 800,600)
organ_index = 0
for hist in hists:
    organ = organs[organ_index][0]
    arm = organs[organ_index][1]
    hist.SetStats(0)
    hist.Draw()
     
    ROOT.gPad.Update()

    stats = ROOT.TPaveStats(0.10, 0.70, 0.30, 0.90, "NDC")
    stats.SetBorderSize(1)
    stats.SetFillStyle(1001)
    stats.SetFillColor(ROOT.kWhite)
    stats.SetTextAlign(12)

    first_bin = hist.FindFirstBinAbove(0)
    xmin = hist.GetBinLowEdge(first_bin)

    last_bin = hist.FindLastBinAbove(0)
    xmax = hist.GetBinLowEdge(last_bin + 1)
    
    stats.AddText(f"{organ}")
    stats.AddText(f"Entries = {int(hist.GetEntries())}")
    stats.AddText(f"Mean = {hist.GetMean():.4f}")
    stats.AddText(f"Std Dev = {hist.GetStdDev():.4f}")
    stats.AddText(f"Min = {xmin}")
    stats.AddText(f"Max = {xmax}")

    stats.Draw()

    ROOT.gPad.Modified()
    ROOT.gPad.Update()

    c.Update()
    if args.showfit == 'no':
        c.SaveAs(f"organ_hists/by_arm/{organ}_arm{arm}_nofit_hist.png")
    else:
        c.SaveAs(f"organ_hists/by_arm/{organ}_arm{arm}_{args.fitfunc}_hist.png")
    organ_index+=1

input("Please press enter to exit...")
