import pytesseract
from logging import basicConfig, INFO

# Настройка логирования
basicConfig(level=INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Настройки Tesseract OCR
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
OCR_LANGUAGE = "rus"
TEMP_IMAGE_PATH = "order.jpg"

# Конфигурация бота
BOT_TOKEN = "7565744604:AAHv2EgDeikKUn_PrJkHv73Xlb_VKeQYE6s"

# URL веб-приложения Google Sheets
SHEETS_WEBAPP_URL = "https://script.google.com/macros/s/AKfycbzJp376LRdvusw_LZgmxN_LeQfU8_EzIcAzzFutFKYs3cM6qRiI0D5B-aM_fV6pfhp6/exec"

# Настройки регулярных выражений для парсинга
REGEX_PATTERNS = {
    "date": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})",
    "usdt": r"Сумма (\d+[.,]\d+)\s*USDT",  # Обновленный паттерн для USDT
    "price": r"Цена (\d+\.?\d*)",
    "amount": r"Сумма (\d+\s?\d*) RUB"
}


