import logging
from config import Config
from collectors.bybit import BybitCollector
from collectors.sheets import SheetsCollector
from exporter import Exporter
from utils.logging_config import setup_logging

def main():
    # Настройка логирования
    setup_logging()
    
    logger = logging.getLogger(__name__)
    logger.info("Starting exporter...")
    
    # Загрузка конфигурации
    config = Config.from_env()
    
    # Инициализация коллекторов
    collectors = [
        BybitCollector(config),
        SheetsCollector(config)
    ]
    
    # Запуск экспортера
    exporter = Exporter(config, collectors)
    exporter.run()

if __name__ == "__main__":
    main() 