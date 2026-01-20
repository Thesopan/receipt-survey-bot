from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def read_receipt(image_path):
    image = Image.open(image_path)
    image = image.convert("L")
    image = image.resize((image.width * 2, image.height * 2))
    image = image.filter(ImageFilter.SHARPEN)
    image = ImageEnhance.Contrast(image).enhance(3.0)
    image = image.convert("RGB")

    # OCR full image
    raw_text = pytesseract.image_to_string(image, config="--psm 6")

    # Crop top 35% for store number
    width, height = image.size
    store_crop = image.crop((0, 0, width, int(height * 0.35)))
    store_text = pytesseract.image_to_string(store_crop, config="--psm 6")

    # Merge both
    combined_text = store_text + "\n" + raw_text

    return combined_text, None
