from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from PIL import Image
import pytesseract
import requests
from config import (
    BOT_TOKEN,
    TESSERACT_PATH,
    OCR_LANGUAGE,
    TEMP_IMAGE_PATH,
    SHEETS_WEBAPP_URL,
    REGEX_PATTERNS
)

# Устанавливаем путь к Tesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

class OrderBot:
    def __init__(self):
        self.webapp_url = SHEETS_WEBAPP_URL

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Привет! Отправьте мне изображение ордера, и я добавлю данные в таблицу.")

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            photo = update.message.photo[-1]
            file = await photo.get_file()
            await file.download_to_drive(TEMP_IMAGE_PATH)
            
            img = Image.open(TEMP_IMAGE_PATH)
            text = pytesseract.image_to_string(img, lang=OCR_LANGUAGE)
            
            # Базовые замены
            replacements = {
                'У5ОТ': 'USDT',
                'у5от': 'USDT',
                'Ш5рТ': 'USDT',
                '/5рТ': 'USDT',
                'ВУВ': 'RUB',
                'ВуУВ': 'RUB',
                'ВВ': 'RUB'
            }
            
            for old, new in replacements.items():
                text = text.replace(old, new)

            # Извлекаем только нужные строки
            lines = text.split('\n')
            filtered_text = []
            for line in lines:
                if any(key in line for key in ['Покупка USDT', 'Завершено', '2024-', 'Сумма', 'Цена', 'Комиссии']):
                    filtered_text.append(line.strip())
            
            text = '\n'.join(filtered_text)
            
            print("\n=== Распознанный текст ===")
            print(text)
            print("===========================")

            data = {
                'date': self._extract_pattern(text, REGEX_PATTERNS['date']),
                'usdt': float(self._extract_pattern(text, REGEX_PATTERNS['usdt'])),
                'price': float(self._extract_pattern(text, REGEX_PATTERNS['price'])),
                'amount': float(self._extract_pattern(text, REGEX_PATTERNS['amount']))
            }
            
            self._send_to_sheets(data)
            await update.message.reply_text("✅ Данные успешно добавлены в таблицу!")
            
        except Exception as e:
            print(f"\n=== Ошибка обработки ===")
            print(f"Тип ошибки: {type(e).__name__}")
            print(f"Текст ошибки: {str(e)}")
            print("========================\n")
            await update.message.reply_text("❌ Не удалось распознать данные. Проверьте изображение.")

    def _extract_pattern(self, text, pattern):
        import re
        match = re.search(pattern, text)
        if not match:
            raise ValueError(f"Не найден паттерн {pattern}")
        # Заменяем запятую на точку и убираем пробелы
        value = match.group(1).replace(' ', '').replace(',', '.')
        return value


    def _send_to_sheets(self, data):
        payload = {
            'action': 'addRow',
            **data
        }
        print("\n=== Отправленные данные ===")
        print(f"Дата: {data['date']}")
        print(f"USDT: {data['usdt']}")
        print(f"Цена: {data['price']}")
        print(f"Сумма: {data['amount']}")
        print("=========================\n")
        
        response = requests.post(self.webapp_url, json=payload)
        if response.status_code != 200:
            raise Exception("Ошибка при отправке данных")

    def run(self):
        application = Application.builder().token(BOT_TOKEN).build()
        
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        
        application.run_polling()
