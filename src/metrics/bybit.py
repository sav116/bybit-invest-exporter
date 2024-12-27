from prometheus_client import Gauge

class BybitMetrics:
    def __init__(self):
        self.total_balance_usdt = Gauge('bybit_total_balance_usdt', 'Total balance in USDT')
        self.account_balance_usdt = Gauge('bybit_account_balance_usdt', 'Balance per account type in USDT', ['account'])
        self.coin_balance = Gauge('bybit_coin_balance', 'Balance per coin', ['coin', 'account'])
        self.coin_value_usdt = Gauge('bybit_coin_value_usdt', 'Value in USDT per coin', ['coin', 'account']) 