import logging
import os
from core.config import SETTINGS

LOG_LEVEL = getattr(logging, SETTINGS.get('log_level', 'INFO'))

# Log dosyası klasörü
LOG_DIR = os.path.join(os.path.dirname(__file__), '../logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'app.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('portfolio_app')
