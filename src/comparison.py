from pathlib import Path
import pandas as pd
import numpy as np

def load_processed_stock_files(processed_dir: str | Path = "data/processed") -> dict[str, pd.DataFrame]:
    """
    Load all processed stock CSV files from the processed data directory.

    Returns
    -------
    dict[str, pd.DataFrame]
        Dictionary where each key is the ticker and each value is its dataframe.
    """

    processed_dir = Path(processed_dir)

    if not processed_dir.exists():
        raise FileNotFoundError(f"Processed directory not found: {processed_dir}")

    csv_files = list(processed_dir.glob("*_processed.csv"))

    if not csv_files:
        raise FileNotFoundError(f"No processed CSV files found in: {processed_dir}")

    stock_data = {}

    for file_path in csv_files:
        data = pd.read_csv(file_path)

        if "Ticker" in data.columns and not data.empty:
            ticker = data["Ticker"].iloc[0]
        else:
            ticker = file_path.stem.replace("_5y_1d_processed", "")

        stock_data[ticker] = data

    return stock_data

def calculate_stock_summary(data: pd.DataFrame, risk_free_rate: float = 0.0) -> dict:
    """
    Calculate summary financial metrics for one stock/index.

    Parameters
    ----------
    data : pd.DataFrame
        Processed stock dataframe.

    risk_free_rate : float
        Annual risk-free rate used for Sharpe ratio.
        Default is 0.0 for simplicity.

    Returns
    -------
    dict
        Summary metrics for the stock.
    """

    required_columns = ["Close", "Daily_Return", "Drawdown"]

    for column in required_columns:
        if column not in data.columns:
            raise ValueError(f"Missing required column: {column}")

    data = data.copy()
    data["Daily_Return"] = pd.to_numeric(data["Daily_Return"], errors="coerce")
    data["Close"] = pd.to_numeric(data["Close"], errors="coerce")
    data["Drawdown"] = pd.to_numeric(data["Drawdown"], errors="coerce")

    data = data.dropna(subset=["Close", "Daily_Return", "Drawdown"])

    if data.empty:
        raise ValueError("No valid data available after cleaning.")

    ticker = data["Ticker"].iloc[0] if "Ticker" in data.columns else "UNKNOWN"

    start_price = data["Close"].iloc[0]
    end_price = data["Close"].iloc[-1]

    total_return = (end_price / start_price) - 1

    num_days = len(data)
    trading_years = num_days / 252

    annualised_return = (1 + total_return) ** (1 / trading_years) - 1 if trading_years > 0 else np.nan

    annualised_volatility = data["Daily_Return"].std() * np.sqrt(252)

    sharpe_ratio = (
        (annualised_return - risk_free_rate) / annualised_volatility
        if annualised_volatility and annualised_volatility > 0
        else np.nan
    )

    max_drawdown = data["Drawdown"].min()

    best_day = data["Daily_Return"].max()
    worst_day = data["Daily_Return"].min()

    positive_days_pct = (data["Daily_Return"] > 0).mean()

    summary = {
        "Ticker": ticker,
        "Start Price": start_price,
        "End Price": end_price,
        "Total Return (%)": total_return * 100,
        "Annualised Return (%)": annualised_return * 100,
        "Annualised Volatility (%)": annualised_volatility * 100,
        "Sharpe Ratio": sharpe_ratio,
        "Maximum Drawdown (%)": max_drawdown * 100,
        "Best Day (%)": best_day * 100,
        "Worst Day (%)": worst_day * 100,
        "Positive Days (%)": positive_days_pct * 100,
        "Observations": num_days
    }

    return summary

def build_comparison_table(
    processed_dir: str | Path = "data/processed",
    risk_free_rate: float = 0.0
) -> pd.DataFrame:
    """
    Build a comparison table for all processed stock/index files.
    """

    stock_data = load_processed_stock_files(processed_dir=processed_dir)

    summaries = []

    for ticker, data in stock_data.items():
        summary = calculate_stock_summary(
            data=data,
            risk_free_rate=risk_free_rate
        )
        summaries.append(summary)

    comparison_df = pd.DataFrame(summaries)

    comparison_df = comparison_df.sort_values(
        by="Total Return (%)",
        ascending=False
    ).reset_index(drop=True)

    return comparison_df

def save_comparison_table(
    comparison_df: pd.DataFrame,
    output_path: str | Path = "data/processed/stock_comparison_summary.csv"
) -> None:
    """
    Save the stock comparison table to CSV.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    comparison_df.to_csv(output_path, index=False)

    print(f"Comparison table saved to {output_path}")
