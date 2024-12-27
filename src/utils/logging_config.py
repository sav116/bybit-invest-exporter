import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logging(log_dir: str = "logs"):
    # Создаем директорию для логов, если её нет
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # Путь к файлу лога
    log_file = log_path / "exporter.log"
    
    # Удаляем старый файл лога при каждом запуске
    if log_file.exists():
        log_file.unlink()
    
    # Настройка форматирования
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Хендлер для файла
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # Хендлер для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Настройка корневого логгера
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Удаляем существующие хендлеры, если они есть
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Добавляем новые хендлеры
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler) 