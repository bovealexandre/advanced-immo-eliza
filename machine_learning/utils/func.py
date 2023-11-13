import numpy as np
from scipy.stats import zscore


def remove_outliers(df, col, threshold):
    z_scores = zscore(df[col])

    outlier_mask = abs(z_scores) > threshold

    df = df[~outlier_mask]
    return df


def price_per_square_meter_per_postal_code(df):
    copied_df = df.copy()

    pivot_table = (
        copied_df.groupby(["postal_code"])
        .apply(lambda x: x["price"].mean() / x["living_area"].mean())
        .reset_index()
    )
    pivot_table.columns = ["postal_code", "price_per_square_meter"]

    pivot_table["price_per_square_meter"] = pivot_table[
        "price_per_square_meter"
    ].replace(np.inf, np.nan)

    pivot_table["average_price_per_postal_code"] = copied_df.groupby("postal_code")[
        "price"
    ].transform("mean")

    pivot_table.to_pickle("features.pkl")
    # df = df.merge(pivot_table, on=["PostalCode"], how="left")
    # return df


def add_year_of_construction(df):
    current_year = 2023  # You can adjust this to the current year
    df["age_of_property"] = current_year - df["year_of_construction"]
    return df
