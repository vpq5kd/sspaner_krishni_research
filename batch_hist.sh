python data_processing_programs/sspaner_histograms_arm_split.py --fitfunc gausian --showfit yes
python data_processing_programs/sspaner_histograms_arm_split.py --fitfunc exponential --showfit yes
python data_processing_programs/sspaner_histograms_arm_split.py --fitfunc exponential --showfit no

git add .
git commit -m "ran batch hists"
git push
