# Bybit P2P Investment Tracker

A Prometheus exporter that tracks P2P investments in Bybit and monitors asset value changes over time. The project combines P2P order history from Google Sheets with real-time balance data from Bybit API.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Docker](https://img.shields.io/badge/docker-supported-blue.svg)

## Overview

This project solves a specific problem: tracking the historical value of crypto investments made through Bybit P2P in relation to the initial fiat currency (RUB). Since Bybit currently doesn't provide an API for P2P order history (promised to be added in the future), we use Google Sheets as a temporary storage for P2P transaction data.

The exporter provides:
- Real-time monitoring of current Bybit account balances
- Historical P2P investment tracking in original fiat currency (RUB)
- Comparison of current asset value vs initial investment
- Prometheus metrics for monitoring and visualization

## Key Features

- Tracks P2P buy/sell orders history from Google Sheets
- Monitors real-time balance and value changes from Bybit
- Calculates total invested amount in original fiat currency
- Shows current portfolio value in both USDT and original fiat
- Supports Docker deployment
- Detailed logging of all transactions and balances

## Metrics

### Investment History (from Google Sheets)
```
# Total amount invested through P2P
total_invested_rub

# Total amount sold through P2P
total_sold_rub

# Net investment (invested - sold)
net_investment_rub
```

### Current Assets (from Bybit API)
```
# Total balance across all accounts
bybit_total_balance_usdt

# Balance per account type
bybit_account_balance_usdt{account="trading|funding|earn"}

# Balance per cryptocurrency
bybit_coin_balance{coin="BTC|ETH|USDT",account="trading|funding|earn"}

# USD value per cryptocurrency
bybit_coin_value_usdt{coin="BTC|ETH|USDT",account="trading|funding|earn"}
```

## Google Sheets Format

The P2P order history sheet should match Bybit's P2P order export format:

| Order No. | Type | Fiat Amount | Currency | Price | Currency | Coin Amount | Cryptocurrency | Transaction Fees | Cryptocurrency |
|-----------|------|-------------|-----------|--------|-----------|-------------|----------------|------------------|----------------|
| 1234567   | BUY  | 50000.00   | RUB      | 93.70  | RUB      | 533.6179   | USDT          | 0               | USDT           |
| 1234568   | SELL | 5000.00    | RUB      | 94.33  | RUB      | 53.0053    | USDT          | 0               | USDT           |

This format exactly matches what you get when manually exporting P2P order history from Bybit's website. Once Bybit adds P2P history to their API, this Google Sheets part can be replaced with direct API calls.

## Configuration

Environment variables:
```bash
PORT=8000                  # Prometheus metrics port
METRICS_INTERVAL=10        # Collection interval in seconds
BYBIT_API_KEY=            # Bybit API key
BYBIT_API_SECRET=         # Bybit API secret
ORDERS_DOC_URL=           # Google Sheets URL with P2P order history
FIAT_CURRENCY=RUB         # Original fiat currency used for P2P trades
```

## Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bybit-investment-exporter.git
cd bybit-investment-exporter
```

2. Create `.env` file with your configuration:
```bash
cp .env.example .env
# Edit .env with your values
```

3. Run with Docker Compose:
```bash
docker-compose up -d
```

### Manual Installation

1. Clone the repository
2. Create and activate virtual environment:
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables
5. Run the exporter:
```bash
python src/main.py
```

## Future Improvements

- Replace Google Sheets with Bybit P2P API once it becomes available
- Add support for multiple fiat currencies
- Add historical price charts and ROI calculations
- Implement alerts for significant value changes

## Acknowledgments

- [Bybit API](https://bybit-exchange.github.io/docs/v5/intro)
- [Prometheus Python Client](https://github.com/prometheus/client_python)
- Community feedback on tracking P2P investments 