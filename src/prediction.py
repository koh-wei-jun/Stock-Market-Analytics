from pathlib import Path
import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def load_processed_stock_data(file_path: str | Path) -> pd.DataFrame:
    """
    Load processed stock data from CSV.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Processed file not found: {file_path}")

    data = pd.read_csv(file_path)

    if "Date" in data.columns:
        data["Date"] = pd.to_datetime(data["Date"], errors="coerce")

    data = data.sort_values("Date").reset_index(drop=True)

    return data

def create_features(data: pd.DataFrame) -> pd.DataFrame:
    """
    Create machine learning features for stock return prediction.
    """

    data = data.copy()

    if "Close" not in data.columns:
        raise ValueError("Missing required column: Close")

    data["Return_1D"] = data["Close"].pct_change(1)
    data["Return_5D"] = data["Close"].pct_change(5)
    data["Return_10D"] = data["Close"].pct_change(10)

    if "MA_20" not in data.columns:
        data["MA_20"] = data["Close"].rolling(window=20).mean()

    data["MA_Ratio"] = data["Close"] / data["MA_20"]

    if "Volatility_20D" not in data.columns:
        data["Daily_Return"] = data["Close"].pct_change()
        data["Volatility_20D"] = data["Daily_Return"].rolling(20).std() * np.sqrt(252)

    data["Target"] = data["Close"].shift(-1) / data["Close"] - 1

    data = data.dropna().reset_index(drop=True)

    return data

def train_test_split_time_series(
    data: pd.DataFrame,
    feature_columns: list[str],
    target_column: str = "Target",
    train_ratio: float = 0.8
):
    """
    Split stock data chronologically into train and test sets.
    """

    if not 0 < train_ratio < 1:
        raise ValueError("train_ratio must be between 0 and 1.")

    split_index = int(len(data) * train_ratio)

    train_data = data.iloc[:split_index].copy()
    test_data = data.iloc[split_index:].copy()

    X_train = train_data[feature_columns]
    X_test = test_data[feature_columns]
    y_train = train_data[target_column]
    y_test = test_data[target_column]

    return X_train, X_test, y_train, y_test, train_data, test_data

def baseline_predict_zero(X_test: pd.DataFrame) -> np.ndarray:
    """
    Baseline model: always predict zero return.
    """

    return np.zeros(len(X_test))

def evaluate_predictions(y_true, y_pred) -> dict:
    """
    Evaluate regression predictions using multiple metrics.
    """

    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    directional_accuracy = (np.sign(y_true) == np.sign(y_pred)).mean()

    return {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
        "Directional_Accuracy": directional_accuracy
    }

def train_linear_regression(X_train, y_train):
    """
    Train a Linear Regression model.
    """

    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def train_random_forest(X_train, y_train, random_state: int = 42):
    """
    Train a Random Forest Regressor.
    """

    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=5,
        random_state=random_state
    )
    model.fit(X_train, y_train)
    return model

def get_predictions_dataframe(
    test_data: pd.DataFrame,
    y_test: pd.Series,
    baseline_pred: np.ndarray,
    linear_pred: np.ndarray,
    rf_pred: np.ndarray
) -> pd.DataFrame:
    """
    Build a dataframe containing actual and predicted returns.
    """

    predictions_df = test_data.copy()

    predictions_df["Actual_Target"] = y_test.values
    predictions_df["Pred_Baseline"] = baseline_pred
    predictions_df["Pred_Linear"] = linear_pred
    predictions_df["Pred_RandomForest"] = rf_pred

    return predictions_df

def run_prediction_pipeline(
    file_path: str | Path,
    train_ratio: float = 0.8
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Full prediction workflow for one stock file.

    Returns
    -------
    feature_data : pd.DataFrame
        Dataset with engineered features.

    results_df : pd.DataFrame
        Model performance comparison table.

    predictions_df : pd.DataFrame
        Test-period actual vs predicted returns.
    """

    data = load_processed_stock_data(file_path)
    feature_data = create_features(data)

    feature_columns = [
        "Return_1D",
        "Return_5D",
        "Return_10D",
        "MA_Ratio",
        "Volatility_20D"
    ]

    X_train, X_test, y_train, y_test, train_data, test_data = train_test_split_time_series(
        data=feature_data,
        feature_columns=feature_columns,
        target_column="Target",
        train_ratio=train_ratio
    )

    model_results = []

    baseline_pred = baseline_predict_zero(X_test)
    baseline_metrics = evaluate_predictions(y_test, baseline_pred)
    baseline_metrics["Model"] = "Baseline_Zero_Return"
    model_results.append(baseline_metrics)

    linear_model = train_linear_regression(X_train, y_train)
    linear_pred = linear_model.predict(X_test)
    linear_metrics = evaluate_predictions(y_test, linear_pred)
    linear_metrics["Model"] = "Linear_Regression"
    model_results.append(linear_metrics)

    rf_model = train_random_forest(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    rf_metrics = evaluate_predictions(y_test, rf_pred)
    rf_metrics["Model"] = "Random_Forest"
    model_results.append(rf_metrics)

    results_df = pd.DataFrame(model_results)
    results_df = results_df[["Model", "MAE", "RMSE", "R2", "Directional_Accuracy"]]

    if "Ticker" in feature_data.columns and not feature_data.empty:
        ticker = feature_data["Ticker"].iloc[0]
    else:
        ticker = Path(file_path).stem.replace("_5y_1d_processed", "")

    results_df["Ticker"] = ticker
    results_df = results_df[["Ticker", "Model", "MAE", "RMSE", "R2", "Directional_Accuracy"]]

    predictions_df = get_predictions_dataframe(
        test_data=test_data,
        y_test=y_test,
        baseline_pred=baseline_pred,
        linear_pred=linear_pred,
        rf_pred=rf_pred
    )

    return feature_data, results_df, predictions_df

def run_prediction_for_all_stocks(
    processed_dir: str | Path = "data/processed",
    output_dir: str | Path = "data/predictions",
    train_ratio: float = 0.8
) -> pd.DataFrame:
    """
    Run prediction pipeline for all processed stock files.

    Saves:
    - engineered features per ticker
    - predictions per ticker
    - model comparison per ticker
    - combined model comparison summary

    Returns
    -------
    pd.DataFrame
        Combined model comparison summary across all tickers.
    """

    processed_dir = Path(processed_dir)
    output_dir = Path(output_dir)

    if not processed_dir.exists():
        raise FileNotFoundError(f"Processed directory not found: {processed_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    csv_files = list(processed_dir.glob("*_processed.csv"))

    if not csv_files:
        raise FileNotFoundError(f"No processed CSV files found in: {processed_dir}")

    all_results = []

    for file_path in csv_files:
        print(f"Running prediction pipeline for {file_path.name}...")

        feature_data, results_df, predictions_df = run_prediction_pipeline(
            file_path=file_path,
            train_ratio=train_ratio
        )

        ticker = results_df["Ticker"].iloc[0]

        feature_output = output_dir / f"{ticker}_features.csv"
        results_output = output_dir / f"{ticker}_model_results.csv"
        predictions_output = output_dir / f"{ticker}_predictions.csv"

        feature_data.to_csv(feature_output, index=False)
        results_df.to_csv(results_output, index=False)
        predictions_df.to_csv(predictions_output, index=False)

        all_results.append(results_df)

        print(f"Saved features to {feature_output}")
        print(f"Saved model results to {results_output}")
        print(f"Saved predictions to {predictions_output}")

    combined_results = pd.concat(all_results, ignore_index=True)

    combined_output = output_dir / "all_tickers_model_comparison.csv"
    combined_results.to_csv(combined_output, index=False)

    print(f"Saved combined model comparison to {combined_output}")

    return combined_results
