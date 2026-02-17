from pd3_template import all_data_df as df
selected_patients_df = df.loc[df["FractionOverlap"] < 0.7, ["Patient","Organ_Clean","FractionOverlap"]]
print(selected_patients_df)
selected_patients_df.to_csv("FV_<_0.7.csv")

selected_patients_df["Patient"] = selected_patients_df["Patient"].str[:2]
print(selected_patients_df["Patient"].unique())
