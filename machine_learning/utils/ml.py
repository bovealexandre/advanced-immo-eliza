import pickle

import optuna
from catboost import CatBoostRegressor
from sklearn.metrics import mean_squared_error, r2_score


def regressor(X_train, X_test, y_train, y_test):
    def train_and_evaluate_catboost(params):
        model = CatBoostRegressor(**params, silent=True)
        model.fit(X_train, y_train, use_best_model=True, eval_set=[(X_test, y_test)])
        predictions = model.predict(X_test)
        r2 = r2_score(y_test, predictions)
        mse = mean_squared_error(y_test, predictions)
        return model, r2, mse

    def objective(trial):
        params = {
            "iterations": 1000,
            "cat_features": [
                "type_of_property",
                "subtype_of_property",
                "kitchen",
                "heating",
                "state_of_property",
                "region",
                "province",
                "neighborhood_type",
                "epc_score",
            ],
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
            "depth": trial.suggest_int("depth", 7, 10),
            "colsample_bylevel": trial.suggest_float("colsample_bylevel", 0.05, 1.0),
            "min_data_in_leaf": trial.suggest_int("min_data_in_leaf", 1, 100),
            "boosting_type": trial.suggest_categorical(
                "boosting_type", ["Ordered", "Plain"]
            ),
            "bootstrap_type": trial.suggest_categorical(
                "bootstrap_type",
                [
                    # "Bayesian", "Bernoulli",
                    "MVS"
                ],
            ),
        }

        if params["bootstrap_type"] == "Bayesian":
            params["bagging_temperature"] = trial.suggest_float(
                "bagging_temperature", 0, 10
            )
        elif params["bootstrap_type"] == "Bernoulli":
            params["subsample"] = trial.suggest_float("subsample", 0.1, 1)

        model, r2, mse = train_and_evaluate_catboost(params)

        if r2 > study.user_attrs.get("best_r2", -1):
            with open("model.pkl", "wb") as model_file:
                pickle.dump(model, model_file)
            study.set_user_attr("best_r2", r2)
            study.set_user_attr("best_mse", mse)

        return mse

    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=30)

    best_r2 = study.user_attrs.get("best_r2", -1)
    best_mse = study.user_attrs.get("best_mse", -1)
    print("Best R-squared:", best_r2)
    print("Best MSE:", best_mse)
