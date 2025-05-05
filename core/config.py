import os
import json
from dotenv import load_dotenv

# .env yükle
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../config/.env'))

# settings.json yükle
with open(os.path.join(os.path.dirname(__file__), '../config/settings.json'), 'r') as f:
    SETTINGS = json.load(f)

# Gizli anahtarlar
SETTINGS['finnhub_api_key'] = os.getenv('FINNHUB_API_KEY')

if not SETTINGS['finnhub_api_key']:
    raise RuntimeError("FINNHUB_API_KEY missing in .env")
