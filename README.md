# Bybit Investment Exporter

A Prometheus exporter that collects and exposes metrics from Bybit cryptocurrency exchange and Google Sheets investment tracking.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Docker](https://img.shields.io/badge/docker-supported-blue.svg)

## Overview

This exporter provides real-time monitoring of:
- Bybit exchange balances across all accounts (Trading, Funding, Earn)
- Investment history tracked in Google Sheets
- Total investment amounts and returns in RUB

## Features

- Real-time balance monitoring from Bybit
- Investment tracking from Google Sheets
- Prometheus metrics export
- Docker support
- Detailed logging
- Configurable update intervals

## Metrics

### Bybit Metrics
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

### Investment Metrics
```
# Total amount invested
total_invested_rub

# Total amount sold
total_sold_rub

# Net investment (invested - sold)
net_investment_rub
```

## Configuration

Environment variables:
```bash
PORT=8000                  # Prometheus metrics port
METRICS_INTERVAL=10        # Collection interval in seconds
BYBIT_API_KEY=            # Bybit API key
BYBIT_API_SECRET=         # Bybit API secret
ORDERS_DOC_URL=           # Google Sheets URL with investment history
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

## Google Sheets Format

The investment tracking sheet should be public and contain these columns:
- `Type` - Transaction type (buy/sell)
- `Fiat Amount` - Transaction amount in RUB

Example:
| Type | Fiat Amount |
|------|-------------|
| buy  | 50000.00    |
| sell | 5000.00     |

## Development

### Project Structure
```
.
├── src/
│   ├── collectors/      # Metric collectors
│   ├── metrics/         # Prometheus metric definitions
│   ├── clients/         # External API clients
│   ├── utils/          # Utility functions
│   ├── config.py       # Configuration handling
│   ├── exporter.py     # Main exporter logic
│   └── main.py         # Application entry point
├── tests/              # Test files
├── docker-compose.yaml # Docker compose configuration
├── Dockerfile         # Docker build configuration
└── requirements.txt   # Python dependencies
```

### Running Tests
```bash
pytest tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Bybit API](https://bybit-exchange.github.io/docs/v5/intro)
- [Prometheus Python Client](https://github.com/prometheus/client_python) 