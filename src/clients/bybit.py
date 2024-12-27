from pybit.unified_trading import HTTP
import logging

logger = logging.getLogger(__name__)

class BybitClient:
    def __init__(self, config):
        self.client = HTTP(
            api_key=config.bybit_api_key,
            api_secret=config.bybit_api_secret
        )

    def get_wallet_balance(self, account_type="UNIFIED"):
        """Получение баланса кошелька для указанного типа аккаунта"""
        return self.client.get_wallet_balance(accountType=account_type)

    def get_coin_price(self, symbol):
        """Получение текущей цены монеты в USDT"""
        if symbol == 'USDT':
            return 1
            
        try:
            ticker = self.client.get_tickers(
                category="spot",
                symbol=f"{symbol}USDT"
            )
            return float(ticker['result']['list'][0]['lastPrice'])
        except Exception as e:
            logger.warning(f"Could not get price for {symbol}: {e}")
            return 0 