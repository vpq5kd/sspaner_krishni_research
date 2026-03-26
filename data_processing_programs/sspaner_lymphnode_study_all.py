import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pd3_template import all_data_df

lymphnode_df = all_data_df[all_data_df["Organ_Clean"] == "LN"].copy()

cols = [
    "V2.0 dosevol",
    "V5.0 dosevol",
    "V10.0 dosevol",
    "V2.0 dosevol/volume",
    "V5.0 dosevol/volume",
    "V10.0 dosevol/volume",
    "Patient",
    "CT#",
    "RTOG"
]

lymphnode_df = lymphnode_df[cols].copy()
lymphnode_df["pt_id"] = lymphnode_df["Patient"].str.replace(r"\d+$", "", regex=True)
lymphnode_df = lymphnode_df.sort_values(["pt_id", "CT#"]).copy()

for i in [2, 5, 10]:
    col = f"V{i}.0 dosevol"
    base = (
        lymphnode_df[lymphnode_df["CT#"] == 0][["pt_id", col]]
        .rename(columns={col: f"V{i}_dosevol_base"})
    )
    lymphnode_df = lymphnode_df.merge(base, on="pt_id", how="left")
    lymphnode_df[f"V{i}_dosevol_delta"] = (
        lymphnode_df[col] - lymphnode_df[f"V{i}_dosevol_base"]
    )
    lymphnode_df[f"V{i}_dosevol_step_delta"] = (
        lymphnode_df.groupby("pt_id")[col].diff()
    )

for i in [2, 5, 10]:
    col = f"V{i}.0 dosevol/volume"
    base = (
        lymphnode_df[lymphnode_df["CT#"] == 0][["pt_id", col]]
        .rename(columns={col: f"V{i}_dosevolvol_base"})
    )
    lymphnode_df = lymphnode_df.merge(base, on="pt_id", how="left")
    lymphnode_df[f"V{i}_dosevolvol_delta"] = (
        lymphnode_df[col] - lymphnode_df[f"V{i}_dosevolvol_base"]
    )
    lymphnode_df[f"V{i}_dosevolvol_step_delta"] = (
        lymphnode_df.groupby("pt_id")[col].diff()
    )

for i in [2, 5, 10]:
    plt.figure(figsize=(8, 6))
    col = f"V{i}.0 dosevol"
    delta_col = f"V{i}_dosevol_delta"

    valid_pts = lymphnode_df.groupby("pt_id")[col].max() > 0
    valid_pts = valid_pts[valid_pts].index
    df_plot = lymphnode_df[lymphnode_df["pt_id"].isin(valid_pts)].copy()

    for pt, group in df_plot.groupby("pt_id"):
        group = group.sort_values("CT#")
        plt.plot(group["CT#"], group[delta_col], alpha=0.2, color="black")

    mean_df = (
        df_plot.groupby("CT#")[delta_col]
        .mean()
        .reset_index()
    )

    plt.plot([], [], color="black", alpha=0.2, label="Patients")
    plt.plot(
        mean_df["CT#"],
        mean_df[delta_col],
        linewidth=4,
        color="purple",
        label="Average"
    )

    plt.xticks(sorted(df_plot["CT#"].unique()))
    plt.xlabel("CT#")
    plt.ylabel(fr"$\Delta$ V{i} (cc)")
    plt.title(f"Change in Lymph Node V{i} Dosevol From Baseline")
    plt.legend()

    filename = f"lymphnode_study/v{i}_dosevol_delta.png"
    plt.savefig(filename, bbox_inches="tight")
    print(f"saved {filename}")
    plt.show()

for i in [2, 5, 10]:
    plt.figure(figsize=(8, 6))
    col = f"V{i}.0 dosevol"
    step_col = f"V{i}_dosevol_step_delta"

    valid_pts = lymphnode_df.groupby("pt_id")[col].max() > 0
    valid_pts = valid_pts[valid_pts].index
    df_plot = lymphnode_df[lymphnode_df["pt_id"].isin(valid_pts)].copy()
    df_plot = df_plot[df_plot["CT#"] != 0]

    for pt, group in df_plot.groupby("pt_id"):
        group = group.sort_values("CT#")
        plt.plot(group["CT#"], group[step_col], alpha=0.2, color="black")

    mean_df = (
        df_plot.groupby("CT#")[step_col]
        .mean()
        .reset_index()
    )

    plt.plot([], [], color="black", alpha=0.2, label="Patients")
    plt.plot(
        mean_df["CT#"],
        mean_df[step_col],
        linewidth=4,
        color="purple",
        label="Average"
    )

    plt.xticks(sorted(df_plot["CT#"].unique()))
    plt.xlabel("CT#")
    plt.ylabel(fr"$\Delta$ step V{i} (cc)")
    plt.title(f"Stepwise Change in Lymph Node V{i} Dosevol")
    plt.legend()

    filename = f"lymphnode_study/v{i}_dosevol_step_delta.png"
    plt.savefig(filename, bbox_inches="tight")
    print(f"saved {filename}")
    plt.show()

for i in [2, 5, 10]:
    plt.figure(figsize=(8, 6))
    col = f"V{i}.0 dosevol/volume"
    delta_col = f"V{i}_dosevolvol_delta"

    valid_pts = lymphnode_df.groupby("pt_id")[col].max() > 0
    valid_pts = valid_pts[valid_pts].index
    df_plot = lymphnode_df[lymphnode_df["pt_id"].isin(valid_pts)].copy()

    for pt, group in df_plot.groupby("pt_id"):
        group = group.sort_values("CT#")
        plt.plot(group["CT#"], group[delta_col], alpha=0.2, color="black")

    mean_df = (
        df_plot.groupby("CT#")[delta_col]
        .mean()
        .reset_index()
    )

    plt.plot([], [], color="black", alpha=0.2, label="Patients")
    plt.plot(
        mean_df["CT#"],
        mean_df[delta_col],
        linewidth=4,
        color="purple",
        label="Average"
    )

    plt.xticks(sorted(df_plot["CT#"].unique()))
    plt.xlabel("CT#")
    plt.ylabel(fr"$\Delta$ V{i} dosevol/volume")
    plt.title(f"Change in Lymph Node V{i} Dosevol/Volume From Baseline")
    plt.legend()

    filename = f"lymphnode_study/v{i}_dosevol_volume_delta.png"
    plt.savefig(filename, bbox_inches="tight")
    print(f"saved {filename}")
    plt.show()

for i in [2, 5, 10]:
    plt.figure(figsize=(8, 6))
    col = f"V{i}.0 dosevol/volume"
    step_col = f"V{i}_dosevolvol_step_delta"

    valid_pts = lymphnode_df.groupby("pt_id")[col].max() > 0
    valid_pts = valid_pts[valid_pts].index
    df_plot = lymphnode_df[lymphnode_df["pt_id"].isin(valid_pts)].copy()
    df_plot = df_plot[df_plot["CT#"] != 0]

    for pt, group in df_plot.groupby("pt_id"):
        group = group.sort_values("CT#")
        plt.plot(group["CT#"], group[step_col], alpha=0.2, color="black")

    mean_df = (
        df_plot.groupby("CT#")[step_col]
        .mean()
        .reset_index()
    )

    plt.plot([], [], color="black", alpha=0.2, label="Patients")
    plt.plot(
        mean_df["CT#"],
        mean_df[step_col],
        linewidth=4,
        color="purple",
        label="Average"
    )

    plt.xticks(sorted(df_plot["CT#"].unique()))
    plt.xlabel("CT#")
    plt.ylabel(fr"$\Delta$ step V{i} dosevol/volume")
    plt.title(f"Stepwise Change in Lymph Node V{i} Dosevol/Volume")
    plt.legend()

    filename = f"lymphnode_study/v{i}_dosevol_volume_step_delta.png"
    plt.savefig(filename, bbox_inches="tight")
    print(f"saved {filename}")
    plt.show()
