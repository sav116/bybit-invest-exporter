from prometheus_client import Gauge

class SheetsMetrics:
    def __init__(self):
        self.total_invested = Gauge('total_invested_rub', 'Total amount invested in RUB')
        self.total_sold = Gauge('total_sold_rub', 'Total amount sold in RUB')
        self.net_investment = Gauge('net_investment_rub', 'Net investment including sales in RUB') 