from pathlib import Path
import pandas as pd
import yfinance as yf

def fetch_stock_data(
    ticker: str,
    period: str = "5y",
    interval: str = "1d",
    save: bool = True
) -> pd.DataFrame:
    """
    Retrieve historical stock market data for a single ticker.

    Parameters
    ----------
    ticker : str
        Stock ticker symbol, for example 'AAPL', 'MSFT', or 'NVDA'.

    period : str
        Length of historical data to retrieve.
        Examples: '1y', '5y', '10y', 'max'.

    interval : str
        Frequency of the data.
        Examples: '1d', '1wk', '1mo'.

    save : bool
        Whether to save the retrieved data as a CSV file.

    Returns
    -------
    pd.DataFrame
        Historical stock price data.
    """

    print(f"Retrieving data for {ticker}...")

    stock = yf.Ticker(ticker)

    data = stock.history(
        period=period,
        interval=interval
    )

    if data.empty:
        raise ValueError(f"No data found for ticker: {ticker}")

    data = data.reset_index()

    data["Ticker"] = ticker

    if save:
        output_dir = Path("data/raw")
        output_dir.mkdir(parents=True, exist_ok=True)

        file_name = f"{ticker}_{period}_{interval}.csv"
        output_path = output_dir / file_name

        data.to_csv(output_path, index=False)

        print(f"Saved {ticker} data to {output_path}")

    return data

def fetch_multiple_stocks(
    tickers: list[str],
    period: str = "5y",
    interval: str = "1d",
    save: bool = True
) -> dict[str, pd.DataFrame]:
    """
    Retrieve historical stock data for multiple tickers.

    Parameters
    ----------
    tickers : list[str]
        List of stock ticker symbols.

    period : str
        Length of historical data to retrieve.

    interval : str
        Frequency of the data.

    save : bool
        Whether to save each stock dataset as a CSV.

    Returns
    -------
    dict[str, pd.DataFrame]
        Dictionary where each key is a ticker and each value is its dataframe.
    """

    all_data = {}

    for ticker in tickers:
        data = fetch_stock_data(
            ticker=ticker,
            period=period,
            interval=interval,
            save=save
        )

        all_data[ticker] = data

    return all_data
