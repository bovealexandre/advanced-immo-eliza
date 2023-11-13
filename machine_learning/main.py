import pandas as pd
import psycopg2
from sklearn.model_selection import train_test_split

from machine_learning.utils.func import (
    price_per_square_meter_per_postal_code,
    remove_outliers,
)
from machine_learning.utils.ml import regressor
from machine_learning.utils.preprocessing import preprocessing


def machine_learning():
    hostname = "localhost"
    username = "postgres"
    password = "postgres"
    database = "properties"

    connection = psycopg2.connect(
        host=hostname, user=username, password=password, database=database
    )
    df = pd.read_sql_query("SELECT * FROM sales", con=connection)

    df = remove_outliers(df, "living_area", 3)

    df = preprocessing(df)

    print(df.shape)

    price_per_square_meter_per_postal_code(df)

    X = df.drop("price", axis=1)
    y = df["price"]

    features = pd.read_pickle("features.pkl")

    X = X.merge(features, on="postal_code", how="left")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    regressor(X_train, X_test, y_train, y_test)
