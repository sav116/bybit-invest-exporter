from .base import BaseCollector
from metrics.sheets import SheetsMetrics
import pandas as pd
import logging
import requests

logger = logging.getLogger(__name__)

class SheetsCollector(BaseCollector):
    def __init__(self, config):
        super().__init__(config)
        self.metrics = SheetsMetrics()

    def collect(self):
        try:
            sheet_id = self.config.orders_doc_url.split('/')[-2]
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
            
            # Читаем CSV из Google Sheets
            df = pd.read_csv(pd.io.common.StringIO(requests.get(csv_url).text), skiprows=1)
            
            # Приводим тип к нижнему регистру для надежности
            df['Type'] = df['Type'].str.lower()
            
            # Фильтруем только строки с buy/sell и конвертируем amount в float
            valid_df = df[df['Type'].isin(['buy', 'sell'])].copy()
            valid_df['Fiat Amount'] = pd.to_numeric(valid_df['Fiat Amount'], errors='coerce')
            
            # Считае�� суммы и округляем до целых чисел
            total_invested = round(valid_df[valid_df['Type'] == 'buy']['Fiat Amount'].sum())
            total_sold = round(valid_df[valid_df['Type'] == 'sell']['Fiat Amount'].sum())
            net_investment = round(total_invested - total_sold)
            
            # Устанавливаем метрики
            self.metrics.total_invested.set(total_invested)
            self.metrics.total_sold.set(total_sold)
            self.metrics.net_investment.set(net_investment)
            
            # Логируем основные показатели
            logger.info(f"\nInvestment Summary:")
            logger.info(f"Total invested: {total_invested:,} RUB")
            logger.info(f"Total sold: {total_sold:,} RUB")
            logger.info(f"Net investment: {net_investment:,} RUB")
            
        except Exception as e:
            logger.error(f"Error processing spreadsheet data: {e}", exc_info=True)
            self.metrics.total_invested.set(0)
            self.metrics.total_sold.set(0)
            self.metrics.net_investment.set(0) 