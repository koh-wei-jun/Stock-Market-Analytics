from pathlib import Path
import pandas as pd
import numpy as np

def load_raw_stock_data(file_path: str | Path) -> pd.DataFrame:
    """
    Load raw stock data from a CSV file.

    Parameters
    ----------
    file_path : str or Path
        Path to the raw CSV file.

    Returns
    -------
    pd.DataFrame
        Loaded stock data.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    data = pd.read_csv(file_path)

    return data

def clean_stock_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw stock data.

    This function:
    - Converts Date column to datetime
    - Sorts data by Date
    - Removes duplicate dates
    - Standardises missing values
    """

    data = data.copy()

    if "Date" not in data.columns:
        raise ValueError("Expected a 'Date' column in the dataset.")

    data["Date"] = pd.to_datetime(data["Date"], errors="coerce", utc=True)
    data["Date"] = data["Date"].dt.tz_localize(None)

    data = data.dropna(subset=["Date"])

    data = data.sort_values("Date")

    data = data.drop_duplicates(subset=["Date"], keep="last")

    numeric_columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Dividends",
        "Stock Splits"
    ]

    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(data[column], errors="coerce")

    data = data.reset_index(drop=True)

    return data

def add_stock_metrics(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add financial analytics metrics to stock data.

    Metrics created:
    - Daily_Return
    - Cumulative_Return
    - MA_20
    - MA_50
    - MA_200
    - Volatility_20D
    - Cumulative_Max
    - Drawdown
    """

    data = data.copy()

    required_columns = ["Close"]

    for column in required_columns:
        if column not in data.columns:
            raise ValueError(f"Missing required column: {column}")

    data["Daily_Return"] = data["Close"].pct_change()

    data["Cumulative_Return"] = (1 + data["Daily_Return"]).cumprod() - 1

    data["MA_20"] = data["Close"].rolling(window=20).mean()
    data["MA_50"] = data["Close"].rolling(window=50).mean()
    data["MA_200"] = data["Close"].rolling(window=200).mean()

    data["Volatility_20D"] = (
        data["Daily_Return"]
        .rolling(window=20)
        .std()
        * np.sqrt(252)
    )

    data["Cumulative_Max"] = data["Close"].cummax()

    data["Drawdown"] = data["Close"] / data["Cumulative_Max"] - 1

    return data

def process_stock_file(
    input_path: str | Path,
    output_dir: str | Path = "data/processed"
) -> pd.DataFrame:
    """
    Full processing pipeline for one raw stock CSV file.

    Loads, cleans, calculates metrics, and saves processed data.
    """

    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    data = load_raw_stock_data(input_path)
    data = clean_stock_data(data)
    data = add_stock_metrics(data)

    output_path = output_dir / input_path.name.replace(".csv", "_processed.csv")

    data.to_csv(output_path, index=False)

    print(f"Processed file saved to {output_path}")

    return data

def process_all_raw_files(
    raw_dir: str | Path = "data/raw",
    output_dir: str | Path = "data/processed"
) -> dict[str, pd.DataFrame]:
    """
    Process all CSV files in the raw data folder.
    """

    raw_dir = Path(raw_dir)

    if not raw_dir.exists():
        raise FileNotFoundError(f"Raw data folder not found: {raw_dir}")

    csv_files = list(raw_dir.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {raw_dir}")

    processed_data = {}

    for file_path in csv_files:
        print(f"Processing {file_path}...")

        data = process_stock_file(
            input_path=file_path,
            output_dir=output_dir
        )

        ticker = data["Ticker"].iloc[0] if "Ticker" in data.columns else file_path.stem
        processed_data[ticker] = data

    return processed_data
