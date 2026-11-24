import pandas as pd
import numpy as np

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import SplineTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def prepare_time_feature(data: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare a numeric time index for spline regression.

    Spline regression needs numerical input.
    We convert the row order into a time index: 0, 1, 2, 3, ...
    """

    data = data.copy()
    data = data.sort_values("Date").reset_index(drop=True)

    data["Time_Index"] = np.arange(len(data))

    return data

def fit_spline_price_model(
    data: pd.DataFrame,
    target_column: str = "Close",
    n_knots: int = 10,
    degree: int = 3
):
    """
    Fit a spline regression model to stock closing prices.

    Parameters
    ----------
    data : pd.DataFrame
        Stock price dataframe with Date and Close columns.

    target_column : str
        Column to model. Usually 'Close'.

    n_knots : int
        Number of spline knots. More knots = more flexible curve.

    degree : int
        Degree of spline. 3 means cubic spline.

    Returns
    -------
    model : sklearn Pipeline
        Fitted spline regression model.

    results : pd.DataFrame
        Original data with fitted values and residuals.

    metrics : dict
        Model evaluation metrics.
    """

    data = prepare_time_feature(data)

    data = data.dropna(subset=[target_column])

    X = data[["Time_Index"]]
    y = data[target_column]

    model = make_pipeline(
        SplineTransformer(
            n_knots=n_knots,
            degree=degree,
            include_bias=False
        ),
        LinearRegression()
    )

    model.fit(X, y)

    fitted_values = model.predict(X)

    results = data.copy()
    results["Spline_Fitted"] = fitted_values
    results["Spline_Residual"] = results[target_column] - results["Spline_Fitted"]

    mae = mean_absolute_error(y, fitted_values)
    rmse = np.sqrt(mean_squared_error(y, fitted_values))
    r2 = r2_score(y, fitted_values)

    metrics = {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
        "N_Knots": n_knots,
        "Degree": degree
    }

    return model, results, metrics
