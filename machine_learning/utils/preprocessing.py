from pandas import CategoricalDtype

from machine_learning.utils.func import add_year_of_construction


def preprocessing(df):
    df = add_year_of_construction(df)

    # kit_cat = CategoricalDtype(
    #     categories=[
    #         "usa uninstalled",
    #         "semi equipped",
    #         "usa semi equipped",
    #         "hyper equipped",
    #         "usa hyper equipped",
    #         "installed",
    #         "usa installed",
    #     ],
    #     ordered=True,
    # )
    df["kitchen"] = df["kitchen"].fillna("unknown")
    # df["Kitchen"] = df["Kitchen"].astype(kit_cat).cat.codes

    # building_state_type = pd.CategoricalDtype(
    #     categories=[
    #         "to be done up",
    #         "to restore",
    #         "to renovate",
    #         "just renovated",
    #         "good",
    #         "as new",
    #     ],
    #     ordered=True,
    # )
    df["state_of_property"] = df["state_of_property"].fillna("unknown")
    # df["StateOfBuilding"] = df["StateOfBuilding"].astype(building_state_type).cat.codes

    # heating_cat = CategoricalDtype(
    #     categories=[
    #         "fueloil",
    #         "gas",
    #         "carbon",
    #         "wood",
    #         "pellet",
    #         "electric",
    #         "solar",
    #     ],
    #     ordered=True,
    # )
    df["heating"] = df["heating"].fillna("unknown")
    # df["heating"] = df["heating"].astype(heating_cat)
    df["neighborhood_type"] = df["neighborhood_type"].fillna("unknown")
    df["epc_score"] = df["epc_score"].fillna("unknown")
    df["furnished"] = df["furnished"].fillna(False)
    df["pools"] = df["pools"].fillna(False)

    df = df.drop(columns=["property_id"], errors="ignore")
    df = df.dropna(subset=["price", "region", "province"])

    return df
