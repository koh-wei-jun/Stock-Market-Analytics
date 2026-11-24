from src.data_collection import fetch_multiple_stocks

def main():
    tickers = [
    "AAPL",   # Apple
    "MSFT",   # Microsoft
    "NVDA",   # NVIDIA
    "AMZN",   # Amazon
    "GOOGL",  # Alphabet (Class A shares)
    "META",   # Meta Platforms
    "TSLA",   # Tesla
    "^GSPC",  # S&P 500 index
]


    stock_data = fetch_multiple_stocks(
        tickers=tickers,
        period="5y",
        interval="1d",
        save=True
    )

    for ticker, data in stock_data.items():
        print("\n" + "=" * 60)
        print(f"{ticker} data preview")
        print("=" * 60)

        print(data.head())

        print("\nDataset shape:")
        print(data.shape)

        print("\nColumns:")
        print(data.columns.tolist())

if __name__ == "__main__":
    main()
