import pandas as pd
import matplotlib.pyplot as plt

from src.advanced_analytics import fit_spline_price_model

def main():
    ticker = "AAPL"
    file_path = "data/processed/AAPL_5y_1d_processed.csv"

    data = pd.read_csv(file_path)

    model, results, metrics = fit_spline_price_model(
        data=data,
        target_column="Close",
        n_knots=12,
        degree=3
    )

    print("Spline Regression Metrics")
    print("=========================")

    for metric, value in metrics.items():
        print(f"{metric}: {value}")

    plt.figure(figsize=(12, 6))
    plt.plot(results["Date"], results["Close"], label="Actual Close", alpha=0.6)
    plt.plot(results["Date"], results["Spline_Fitted"], label="Spline Fitted Trend", linewidth=2)

    plt.title(f"{ticker} Closing Price with Spline Regression Trend")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
