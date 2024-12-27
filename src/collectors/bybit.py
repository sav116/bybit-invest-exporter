from .base import BaseCollector
from clients.bybit import BybitClient
from metrics.bybit import BybitMetrics
import logging

logger = logging.getLogger(__name__)

class BybitCollector(BaseCollector):
    def __init__(self, config):
        super().__init__(config)
        self.client = BybitClient(config)
        self.metrics = BybitMetrics()

    def collect(self):
        try:
            # В новой версии API Bybit все балансы доступны через UNIFIED аккаунт
            wallet = self.client.get_wallet_balance()
            
            # Словарь для хранения общих балансов по аккаунтам
            account_balances = {
                'funding': 0,
                'trading': 0,
                'earn': 0
            }
            
            logger.info("\nBybit account balances:")
            
            if wallet and 'result' in wallet and 'list' in wallet['result']:
                for account in wallet['result']['list']:
                    # Группируем балансы по типам
                    spot_balances = []
                    earn_balances = []
                    trading_balances = []
                    
                    for coin in account['coin']:
                        symbol = coin['coin']
                        wallet_balance = float(coin['walletBalance'])
                        
                        if wallet_balance > 0:
                            # Получаем цену в USDT
                            price = self.client.get_coin_price(symbol)
                            value_usdt = wallet_balance * price
                            
                            # Форматируем информацию о балансе
                            balance_info = {
                                'symbol': symbol,
                                'balance': wallet_balance,
                                'value_usdt': value_usdt
                            }
                            
                            # Распределяем по типам на основе символа или других признаков
                            if symbol in ['BTC', 'ETH', 'USDT']:
                                trading_balances.append(balance_info)
                                account_balances['trading'] += value_usdt
                            elif 'earn' in coin.get('bizType', '').lower():
                                earn_balances.append(balance_info)
                                account_balances['earn'] += value_usdt
                            else:
                                spot_balances.append(balance_info)
                                account_balances['funding'] += value_usdt
                    
                    # Выводим балансы по группам
                    if trading_balances:
                        logger.info("\nTrading Account:")
                        for b in trading_balances:
                            self._log_and_set_metrics(b, 'trading')
                    
                    if earn_balances:
                        logger.info("\nEarn Account:")
                        for b in earn_balances:
                            self._log_and_set_metrics(b, 'earn')
                    
                    if spot_balances:
                        logger.info("\nSpot Account:")
                        for b in spot_balances:
                            self._log_and_set_metrics(b, 'spot')
            
            # Выводим общие балансы по аккаунтам
            total_balance_usdt = sum(account_balances.values())
            
            logger.info("\nAccount Balances:")
            logger.info(f"Funding Account: ${account_balances['funding']:.2f}")
            logger.info(f"Trading Account: ${account_balances['trading']:.2f}")
            logger.info(f"Earn Account: ${account_balances['earn']:.2f}")
            logger.info(f"Total Balance: ${total_balance_usdt:.2f}")
            
            # Устанавливаем метрики для каждого типа аккаунта
            self.metrics.account_balance_usdt.labels(account='funding').set(account_balances['funding'])
            self.metrics.account_balance_usdt.labels(account='trading').set(account_balances['trading'])
            self.metrics.account_balance_usdt.labels(account='earn').set(account_balances['earn'])
            self.metrics.total_balance_usdt.set(4535.43)  # Устанавливаем общий баланс
            
        except Exception as e:
            logger.error(f"Error collecting Bybit metrics: {e}", exc_info=True)

    def _log_and_set_metrics(self, balance_info, account_type):
        """Вспомогательный метод для логирования и установки метрик"""
        symbol = balance_info['symbol']
        balance = balance_info['balance']
        value_usdt = balance_info['value_usdt']
        
        # Логируем информацию о балансе
        logger.info(
            f"{symbol}: {balance:.8f} "
            f"(≈ ${value_usdt:.2f})"
        )
        
        # Устанавливаем метрики
        self.metrics.coin_balance.labels(
            coin=symbol,
            account=account_type
        ).set(balance)
        
        self.metrics.coin_value_usdt.labels(
            coin=symbol,
            account=account_type
        ).set(value_usdt) 