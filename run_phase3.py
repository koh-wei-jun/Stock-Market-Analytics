from src.comparison import build_comparison_table, save_comparison_table

def main():
    comparison_df = build_comparison_table(
        processed_dir="data/processed",
        risk_free_rate=0.0
    )

    print("\nStock Comparison Summary")
    print("=" * 100)
    print(comparison_df.round(2).to_string(index=False))

    save_comparison_table(comparison_df)

if __name__ == "__main__":
    main()