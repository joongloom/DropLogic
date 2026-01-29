import requests
import logging
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class BaseExtractor:
    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(name)
        self.session = self._create_session()

    def _create_session(self):
        session = requests.Session()
        
        retry_strategy = Retry(
            total=3,
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        
        session.headers.update({
            "User-Agent": "CryptoIntelligenceBot/1.0",
            "Content-Type": "application/json"
        })
        
        return session

    def get(self, url, params=None, headers=None):
        try:
            self.logger.info(f"Запрос к {url} с параметрами {params}")
            response = self.session.get(url, params=params, headers=headers, timeout=15)
            
            response.raise_for_status()
            
            return response.json()
        
        except requests.exceptions.HTTPError as http_err:
            self.logger.error(f"HTTP ошибка при запросе к {url}: {http_err}")
        except Exception as err:
            self.logger.error(f"Другая ошибка при запросе к {url}: {err}")
        
        return None