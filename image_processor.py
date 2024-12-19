
from PIL import Image
import pytesseract
import re
from config import TEMP_IMAGE_PATH, OCR_LANGUAGE

class ImageProcessor:
    @staticmethod
    def extract_text_from_image(image_path):
        img = Image.open(image_path)
        return pytesseract.image_to_string(img, lang=OCR_LANGUAGE)
    
    @staticmethod
    def parse_order_text(text):
        try:
            date = re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", text).group()
            usdt = float(re.search(r"(\d+\.\d+) USDT", text).group(1))
            price = float(re.search(r"Цена:\s*(\d+)", text).group(1))
            amount = float(re.search(r"Сумма:\s*(\d+)", text).group(1))
            
            return {
                "date": date,
                "usdt": usdt,
                "price": price,
                "amount": amount
            }
        except Exception:
            return None
