import time
import logging
from prometheus_client import start_http_server

logger = logging.getLogger(__name__)

class Exporter:
    def __init__(self, config, collectors):
        self.config = config
        self.collectors = collectors

    def collect_metrics(self):
        for collector in self.collectors:
            try:
                collector.collect()
            except Exception as e:
                logger.error(f"Error collecting metrics for {collector.__class__.__name__}: {e}")

    def run(self):
        start_http_server(self.config.port)
        logger.info(f"Exporter started on port {self.config.port}")
        
        while True:
            try:
                self.collect_metrics()
                time.sleep(self.config.metrics_interval)
            except Exception as e:
                logger.error(f"Error collecting metrics: {e}")
                time.sleep(5) 