from src.prediction import run_prediction_for_all_stocks

def main():
    combined_results = run_prediction_for_all_stocks(
        processed_dir="data/processed",
        output_dir="data/predictions",
        train_ratio=0.8
    )

    print("\nPhase 4 Upgrade: All Tickers Model Comparison")
    print("=" * 100)
    print(combined_results.round(6).to_string(index=False))

if __name__ == "__main__":
    main()
