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

### Phase 3: Financial Comparison

The platform will compare stocks using metrics such as:


Metric	Purpose
Total Return	Measures full-period percentage gain or loss
Annualised Return	Converts total return into yearly performance
Annualised Volatility	Measures yearly return fluctuation
Sharpe Ratio	Measures risk-adjusted return
Maximum Drawdown	Measures worst peak-to-trough decline
Best Day	Highest daily return
Worst Day	Lowest daily return
Positive Days %	Percentage of trading days with positive return
This phase will help answer questions such as:

Which Magnificent Seven stock performed best historically?
Which stock was most volatile?
Did higher returns come with higher risk?
How did each stock compare against the S&P 500?

### Phase 4: Machine Learning and Advanced Analytics
The platform will include machine learning models to estimate future stock returns or prices.

Planned models include:

Linear Regression
Random Forest Regressor
Gradient Boosting Regressor
Spline Regression
Spline regression may be used for:

Nonlinear trend smoothing
Modelling historical price trends
Analysing nonlinear relationships between indicators and future returns
Comparing against simpler models
Evaluation metrics may include:

Mean Absolute Error, MAE
Root Mean Squared Error, RMSE
R² score
Directional accuracy
Baseline comparison
Important modelling principles:

Use chronological train/test splits.
Avoid random shuffling of time-series data.
Avoid look-ahead bias.
Compare model performance against simple baselines.

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
