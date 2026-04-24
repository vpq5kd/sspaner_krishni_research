import pandas as pd

df = pd.read_csv("persisted_data/delta_dosevol.csv")
dose_order = ["V2", "V5", "V10"]

df["dose"] = pd.Categorical(df["dose"], categories=dose_order, ordered=True)
pivot = df.pivot_table(
    index=["organ", "dose"],
    columns="arm",
    values=["mean", "std", "range", "min", "max"]
)

# flatten multiindex columns
pivot.columns = [
    f"A{arm}_{metric}" for metric, arm in pivot.columns
]

pivot = pivot.reset_index()
pivot = pivot.round(3)

pivot.to_csv("persisted_data/delta_dosevol.csv")
