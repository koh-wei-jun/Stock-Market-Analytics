from src.stock_analysis import process_all_raw_files

def main():
    processed_data = process_all_raw_files(
        raw_dir="data/raw",
        output_dir="data/processed"
    )

    print("\nPhase 2 completed successfully.")
    print("Processed tickers:")

    for ticker, data in processed_data.items():
        print(f"- {ticker}: {data.shape[0]} rows, {data.shape[1]} columns")

        print(data[
            [
                "Date",
                "Ticker",
                "Close",
                "Daily_Return",
                "Cumulative_Return",
                "MA_20",
                "MA_50",
                "Volatility_20D",
                "Drawdown"
            ]
        ].tail())

if __name__ == "__main__":
    main()
