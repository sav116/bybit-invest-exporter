from environs import Env
from dataclasses import dataclass

@dataclass
class Config:
    port: int
    metrics_interval: int
    bybit_api_key: str
    bybit_api_secret: str
    orders_doc_url: str

    @classmethod
    def from_env(cls) -> 'Config':
        env = Env()
        env.read_env()

        return cls(
            port=env.int('PORT', 8000),
            metrics_interval=env.int('METRICS_INTERVAL', 10),
            bybit_api_key=env.str('BYBIT_API_KEY'),
            bybit_api_secret=env.str('BYBIT_API_SECRET'),
            orders_doc_url=env.str('ORDERS_DOC_URL')
        ) 