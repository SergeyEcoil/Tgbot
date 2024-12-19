import requests
from config import SHEETS_WEBAPP_URL

class SheetsManager:
    def __init__(self):
        self.webapp_url = SHEETS_WEBAPP_URL
    
    def add_order(self, data):
        payload = {
            'date': data["date"],
            'usdt': data["usdt"],
            'price': data["price"],
            'amount': data["amount"],
            'action': 'addRow'
        }
        
        response = requests.post(self.webapp_url, json=payload)
        return response.status_code == 200
