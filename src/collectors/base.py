from abc import ABC, abstractmethod
from config import Config

class BaseCollector(ABC):
    def __init__(self, config: Config):
        self.config = config

    @abstractmethod
    def collect(self):
        """Collect metrics"""
        pass 