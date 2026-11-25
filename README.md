# Stock Market Intelligence Platform

A Business Analytics portfolio project built with Python to retrieve, analyse, compare and eventually predict US stock market performance.

This project is designed to go beyond a simple stock price tracker. It aims to demonstrate practical skills in data collection, data cleaning, exploratory data analysis, financial analytics, machine learning, database management and dashboard development.

## Project Status

Current progress:

- Phase 1: Historical stock data collection — in progress/completed
- Phase 2: Data cleaning and stock performance metrics — planned/started
- Phase 3: Financial comparison and risk analytics — planned
- Phase 4: Machine learning and advanced analytics — planned
- Phase 5: SQL Server integration — planned
- Phase 6: Streamlit dashboard — planned

## Tracked Market Universe

The platform tracks the Magnificent Seven stocks and the S&P 500 benchmark.

| Ticker | Company / Index |
|---|---|
| AAPL | Apple |
| MSFT | Microsoft |
| NVDA | NVIDIA |
| AMZN | Amazon |
| GOOGL | Alphabet |
| META | Meta Platforms |
| TSLA | Tesla |
| ^GSPC | S&P 500 Index |

The S&P 500 is included as a benchmark to compare individual stock performance against the broader US market.

## Project Objectives

The final platform aims to:

1. Retrieve real historical US stock market data.
2. Store raw and processed stock data.
3. Analyse stock performance using Python.
4. Compare companies using financial and risk metrics.
5. Apply machine learning to estimate future returns or prices.
6. Evaluate prediction models against simple baselines.
7. Store stock market data and analysis results in SQL Server.
8. Display insights through an interactive Streamlit dashboard.
9. Include advanced analytics such as spline regression for nonlinear trend analysis.

## Current Features

### Phase 1: Data Collection

Implemented historical stock data retrieval using `yfinance`.

The data collection module can:

- Retrieve stock data for a single ticker.
- Retrieve stock data for multiple tickers.
- Download daily historical stock data.
- Save raw stock data as CSV files.
- Add a ticker column to each dataset.

Raw data is saved in:
data/raw/

### Phase 2: Stock Analysis
A stock analysis module has been planned/started to process raw data and calculate financial metrics.

Planned metrics include:

- Daily return
- Cumulative return
- 20-day moving average
- 50-day moving average
- 200-day moving average
- 20-day annualised volatility
- Cumulative maximum price
- Drawdown
- Processed data will be saved in:


data/processed/
Example processed files:

data/processed/AAPL_5y_1d_processed.csv
data/processed/MSFT_5y_1d_processed.csv
data/processed/NVDA_5y_1d_processed.csv

## Planned Features

## Phase 3: Financial Comparison and Risk Metrics

Phase 3 extends the project from simple stock data retrieval into comparative financial analytics. The purpose of this phase is to evaluate the historical performance and risk characteristics of the tracked stocks and benchmark using structured metrics rather than relying only on price charts.

### Objective

The objective of Phase 3 is to compare the Magnificent Seven stocks and the S&P 500 using key performance and risk indicators. This allows the project to answer practical analytics questions such as:

- Which stock delivered the strongest historical return?
- Which stock experienced the highest volatility?
- Did higher return come with higher risk?
- How did each stock compare against the S&P 500 benchmark?
- Which stocks experienced the most severe drawdowns?

### Input Data

Phase 3 uses the processed datasets generated in Phase 2. These files are stored in:
data/processed/

Each processed dataset contains cleaned historical stock data and derived metrics such as:

- Daily_Return
- Cumulative_Return
- MA_20
- MA_50
- MA_200
- Volatility_20D
- Drawdown
- Implementation
- A new comparison module was created in:


### src/comparison.py
This module performs the following tasks:

- Loads all processed stock CSV files from data/processed/
- Calculates summary performance and risk metrics for each ticker
- Combines the results into one comparison table
- Saves the final summary table as a CSV file
- A runner script was created in:

### run_phase3.py
This script executes the full comparison workflow and prints the summary table in the terminal.

Metrics Calculated
The following metrics are calculated for each stock or index:


Metric	Description
Total Return (%)	Overall percentage gain or loss over the full dataset period
Annualised Return (%)	Average yearly growth rate based on the full historical period
Annualised Volatility (%)	Standard deviation of daily returns scaled to an annual basis
Sharpe Ratio	Risk-adjusted return using annualised return divided by annualised volatility
Maximum Drawdown (%)	Largest decline from a historical peak
Best Day (%)	Highest single-day return
Worst Day (%)	Lowest single-day return
Positive Days (%)	Percentage of trading days with positive returns
Observations	Number of valid trading-day observations used in the analysis
Business Analytics Value
This phase is important because it transforms the project into a more meaningful comparative analysis tool. Instead of asking only how prices changed, the project can now evaluate return, risk and consistency across different stocks.

This supports Business Analytics concepts such as:

historical performance evaluation
risk measurement
comparative analysis
benchmark-based analysis
interpretation of trade-offs between return and volatility
Output
The main output of Phase 3 is a stock comparison summary file:


### data/processed/stock_comparison_summary.csv
This file can later be used in the Streamlit dashboard to display ranking tables, comparison charts and risk summaries.

Key Learning Outcome
By completing Phase 3, the project demonstrates the ability to move from raw data collection to structured financial analysis. It also creates a reusable analytics layer that supports later phases such as machine learning, portfolio analytics and interactive dashboard reporting.




### Phase 4: Machine Learning and Advanced Analytics
The platform will include machine learning models to estimate future stock returns or prices.

Phase 4 introduces predictive analytics into the project. The purpose of this phase is to test whether historical stock features can be used to estimate next-day stock returns and to evaluate whether the resulting models are meaningfully better than a simple baseline.

### Objective

The objective of Phase 4 is to build and evaluate machine learning models that predict the next trading day’s stock return. This phase is designed as an experiment in predictive modelling rather than as a trading system.

The key questions addressed include:

Can historical stock indicators help estimate future returns?
Are machine learning models more useful than a baseline assumption of zero return?
Which model performs better across different stocks?
Are some stocks more predictable than others?
Is prediction accuracy strong enough to be practically meaningful?
Prediction Target
Instead of predicting raw future prices, the project predicts the next-day return:


Target = Tomorrow's Close / Today's Close - 1
This approach is used because returns are more consistent and comparable across stocks than raw prices.

Input Data
Phase 4 uses the processed stock files from:


data/processed/
These processed files already contain the cleaned price history and technical indicators calculated in Phase 2.

### Implementation
A prediction module was created in:

src/prediction.py
This module performs the following tasks:

Loads a processed stock file
Creates predictive features from historical stock data
Creates the next-day return target variable
Splits the dataset chronologically into training and testing sets
Trains machine learning models
Evaluates model performance using multiple metrics
Saves model outputs for each ticker
Two runner scripts were used during development:


run_phase4.py
run_phase4_all.py
The first script was used to test the pipeline on a single stock, while the upgraded version processes all tracked stocks and the S&P 500 benchmark.

### Features Engineered
The following features were created for the prediction models:

Feature	Description
Return_1D	Percentage return over the last 1 trading day
Return_5D	Percentage return over the last 5 trading days
Return_10D	Percentage return over the last 10 trading days
MA_Ratio	Ratio of closing price to the 20-day moving average
Volatility_20D	20-day rolling annualised volatility
These features were chosen to capture recent momentum, mean reversion and short-term market risk.

### Modelling Approach
The following models were implemented:

Model	Purpose
Baseline Zero Return	Predicts zero return for every test observation
Linear Regression	Provides a simple linear benchmark
Random Forest Regressor	Captures more complex nonlinear relationships
The baseline model is especially important because it provides a simple reference point. If a machine learning model cannot outperform a zero-return baseline, then its practical usefulness is questionable.

### Time-Series Validation
A chronological train/test split was used instead of random shuffling.

This is necessary because stock data is time-series data. Random shuffling would allow future information to leak into the training process, leading to unrealistic results. By training on earlier observations and testing on later observations, the project follows a more valid financial forecasting approach.

### Evaluation Metrics
The following metrics were used to evaluate model performance:

Metric	Description
MAE	Mean Absolute Error
RMSE	Root Mean Squared Error
R²	Proportion of variation explained by the model
Directional Accuracy	Percentage of test cases where the model predicted the correct direction of return
These metrics allow the project to evaluate both numerical prediction error and directional usefulness.

### Upgraded Phase 4 Workflow
Phase 4 was later upgraded so that the full pipeline could be run across all tracked stocks, rather than only one stock.

The upgraded pipeline now:

Reads all processed stock files from data/processed/
Runs the prediction workflow for each ticker
Saves engineered features for each ticker
Saves model results for each ticker
Saves actual vs predicted test-period returns for each ticker
Creates one combined model comparison file across all tickers

### Phase 5: SQL Server Integration
The platform will eventually store data in SQL Server.

Planned database features:

Store historical stock prices.
Store processed analytics metrics.
Query stock data by ticker and date.
Integrate SQL Server with Python.
Demonstrate database design and data management skills.
Possible database:


CREATE DATABASE StockAnalyticsDB;
Possible table:


CREATE TABLE StockPrices (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Ticker VARCHAR(10),
    TradeDate DATE,
    OpenPrice FLOAT,
    HighPrice FLOAT,
    LowPrice FLOAT,
    ClosePrice FLOAT,
    Volume BIGINT
);

### Phase 6: Streamlit Dashboard
The final application will be built using Streamlit.

Planned dashboard sections:


Page	Description
Overview	Latest stock prices and historical performance
Stock Analysis	Moving averages, returns, volatility and drawdowns
Company Comparison	Compare Magnificent Seven stocks against the S&P 500
Prediction	Machine learning predictions and evaluation metrics
Advanced Analytics	Spline regression and nonlinear trend analysis
Portfolio Analytics	Portfolio returns, volatility and risk
Project Structure
Current/recommended structure:


Stock-Market-Analytics/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── models/
│
├── src/
│   ├── __init__.py
│   ├── data_collection.py
│   ├── stock_analysis.py
│   ├── prediction.py
│   ├── advanced_analytics.py
│   └── database.py
│
├── dashboard/
│   └── app.py
│
├── main.py
├── run_phase2.py
├── run_spline_analysis.py
├── requirements.txt
└── README.md
Technologies Used

Technology	Purpose
Python	Main programming language
pandas	Data manipulation and analysis
NumPy	Numerical calculations
yfinance	Historical stock data retrieval
Matplotlib	Static visualisations
Plotly	Interactive visualisations
Scikit-learn	Machine learning and spline regression
SQL Server	Database storage
SQLAlchemy / pyodbc	Python-to-SQL Server connection
Streamlit	Interactive dashboard
VS Code	Development environment
GitHub	Version control and portfolio showcase
Setup Instructions
1. Clone or open the project folder

cd Stock-Market-Analytics
2. Create a virtual environment

python -m venv .venv
3. Activate the virtual environment
For Git Bash on Windows:


source .venv/Scripts/activate
For Windows PowerShell:


.venv\Scripts\Activate.ps1
For macOS/Linux:


source .venv/bin/activate
4. Install required packages

pip install -r requirements.txt
Running the Project
Phase 1: Retrieve historical stock data

python main.py
This downloads historical data for the selected tickers and saves CSV files into:


data/raw/
Phase 2: Process stock data

python run_phase2.py
This loads the raw CSV files, calculates stock analytics metrics, and saves processed data into:


data/processed/
Advanced Analytics: Spline regression

python run_spline_analysis.py
This will eventually run spline regression analysis on selected stock data.

Example Analytical Questions
This project is intended to answer questions such as:

Which Magnificent Seven stock had the highest total return over the past five years?
Which stock had the highest annualised volatility?
How did each stock perform compared with the S&P 500?
Which stocks experienced the largest drawdowns?
Are moving averages useful for understanding stock trends?
Can machine learning models estimate future returns better than a simple baseline?
Does spline regression reveal useful nonlinear historical trends?
How risky would a portfolio of Magnificent Seven stocks have been historically?
Relationship to Business Analytics
This project supports skills relevant to Business Analytics, including:


Business Analytics Area	Project Application
Python Programming	Data retrieval, analysis and modelling
Data Management	Raw and processed dataset organisation
Database Management	SQL Server storage and querying
Statistics	Returns, volatility, drawdown and risk
Machine Learning	Predictive modelling and evaluation
Business Forecasting	Return and price forecasting experiments
Data Visualisation	Charts and Streamlit dashboard
Decision Analytics	Portfolio risk and performance comparison
